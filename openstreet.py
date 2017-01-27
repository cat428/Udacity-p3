import xml.etree.cElementTree as ET
import re
import pprint
import codecs
import json
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
dashzip = re.compile(r'^(\d{5})-\d{4}$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
expected=["Road", "Highway", "Street", "Avenue", "Parkway", "Drive", "Place", "Court", "Boulevard", "Lane", "Way", "Loop", "Circle"]
Mapping={"Rd":"Road", "Hwy":"Highway", "highway":"Highway", "St.":"Street", "Ave":"Avenue", "St":"Street", "Pkwy":"Parkway", "road":"Road", "Dr":"Drive"}

def shape_element(element):
	"""
	Shape the element into dictionary
	part of it is from the lesson but I adjusted a huge part of this function

	Args:
		elements 

	Returns: 
		node as dictionary
	"""
	node = {}
	address = {}
	creat = {}
	building = {}
	telescope = {}
	lane = {}
	roof = {} 
	pos = []
	if element.tag == "node" or element.tag == "way" :
		for key, value in element.attrib.iteritems():
			if key in CREATED:
				creat[key]=value
			elif key == "lat" or key == "lon":
				pos.append(float(value))
			else:
				node[key] = value
			if pos:
				node['pos'] = pos
			if creat:
				node['created'] = creat
			
		for tag in element.iter("tag"):
			if lower.match(tag.attrib['k']):
				node[tag.attrib['k']] = tag.attrib['v']
			elif lower_colon.match(tag.attrib['k']):
				first_word = tag.attrib['k'].split(':')[0]
				if first_word == 'addr':
					nodeup = nodeupdate(tag)
					address.update(nodeup)
				elif first_word == 'building':
					nodeup = nodeupdate(tag)
					building.update(nodeup)
				elif first_word == 'lane':
					nodeup = nodeupdate(tag)
					lane.update(nodeup)
				elif first_word == 'telescope':
					nodeup = nodeupdate(tag)
					telescope.update(nodeup)
				elif first_word == 'roof':
					nodeup = nodeupdate(tag)
					roof.update(nodeup)

				if telescope:
					node['telescope'] = telescope
				if roof:
					node['roof'] = roof
				if building:
					node['building_details'] = building
				if address:
					node['address'] = address

		return node

	else:
		return None

def nodeupdate(tag):
	"""
	update the subset of elements as a dictionary

	Args:
		tag(xml elements)

	Returns:
		node(dictionary)

	"""
	node = {}
	last_word = tag.attrib['k'].split(':')[-1]

	if last_word == "street":
		if last_word not in expected:
			tag.attrib['v'] = updatestreet(tag.attrib['v'], last_word)
	elif last_word == 'postcode':
		if dashzip.match(tag.attrib['v']):
			zip = tag.attrib['v'].split('-')[0]
			tag.attrib['v'] = zip
	elif last_word == 'colour':
		last_word = 'color'

	node[last_word] = tag.attrib['v']
  
	return node


def process_map(file_in):
	"""
	Write the dictionary into the output Json file
	This part is from the lesson

	Args:
		file_in(xml)
	Returns:
		data(json)
	"""
	file_out = "{0}.json".format(file_in)
	data = []
	with codecs.open(file_out, "w") as fo:
		for _, element in ET.iterparse(file_in):
			el = shape_element(element)
			if el:
				data.append(el)
				fo.write(json.dumps(el) + "\n")
	return data

def audit(filename):
	"""
	audit the street names to check whether there are any irregulars

	Args:
		filename(xml)
	Returns:
		streettype(dictionary), oddstreetname(set)
	"""
	context = ET.iterparse(filename)
	streettype = dict()
	oddstreetname = set()
	for event, elem in context:
		 if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				 if tag.attrib['k'] == "addr:street":
					lastword = tag.attrib['v'].split()[-1]
					if lastword not in expected:
						 oddstreetname.add(tag.attrib['v'])
					if lastword in streettype:
						 streettype[lastword] = streettype[lastword]+1
					else:
						 streettype[lastword] = 1
	return streettype, oddstreetname

def updatestreet(street, lastword):
	"""
	update street names

	Args:
		street(str), lastword(str)
	Returns:
		street(str)
	"""
	if lastword in Mapping:
		street = street.replace(lastword, Mapping[lastword])

	return street


def auditzipcode(filename):
	"""
	audit the zipcodes

	Args:
		filename(xml)
	Returns:
		zipcode(dict)
	"""
	zipcode = dict()
	context = ET.iterparse(filename)
	for event, elem in context:
		if elem.tag == "node" or elem.tag == "way":
			for el in elem.iter("tag"):
				if el.attrib['k'] == "addr:postcode":
					if el.attrib['v'] not in zipcode:
						zipcode[el.attrib['v']] = 1
					else:
						zipcode[el.attrib['v']] = zipcode[el.attrib['v']]+1
	return zipcode

def audittag(filename):
	"""
	audit the tags

	Args:
		filename(xml)
	Returns:
		tag(dict)
	"""
	tag = dict()
	context = ET.iterparse(filename)
	for event, elem in context:
		if elem.tag == "node" or elem.tag == "way":
			for el in elem.iter("tag"):
				if el.attrib['k'] not in tag:
					tag[el.attrib['k']] = 1
				else:
					tag[el.attrib['k']] = tag[el.attrib['k']]+1
	return tag


def main():
	tree = "hawaii-latest.osm"
	zip = auditzipcode(tree)
	tag = audittag(tree)
	type, name = audit(tree)
	datajson = process_map(tree)


if __name__=='__main__':
	main()