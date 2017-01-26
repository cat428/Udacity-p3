import xml.etree.cElementTree as ET
import re
import pprint
import codecs
import json
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
dashzip = re.compile(r'^([0-9]|_)*-([0-9]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
expected=["Road", "Highway", "Street", "Avenue", "Parkway", "Drive", "Place", "Court", "Boulevard", "Lane", "Way", "Loop", "Circle"]
Mapping={"Rd":"Road", "Hwy":"Highway", "highway":"Highway", "St.":"Street", "Ave":"Avenue", "St":"Street", "Pkwy":"Parkway", "road":"Road", "Dr":"Drive"}

#part of it is from the lesson but I adjusted a huge part of this function
def shape_element(element):
    node = {}
    address={}
    creat={}
    building={}
    telescope={}
    roof={}
    pos=[]
    if element.tag == "node" or element.tag == "way" :
        for key, value in element.attrib.iteritems():
            if key in CREATED:
                creat[key]=value
            elif key=="lat" or key=="lon":
                pos.append(float(value))
            else:
                node[key]=value
            if pos:
                node['pos']=pos
            if creat:
                node['created']=creat
            
        for tag in element.iter("tag"):
            if lower.match(tag.attrib['k']):
                node[tag.attrib['k']]=tag.attrib['v']
            elif lower_colon.match(tag.attrib['k']):
                if tag.attrib['k']=="addr:street":
                	lastword=tag.attrib['v'].split()[-1]
                	if lastword not in expected:
                		tag.attrib['v']=updatestreet(tag.attrib['v'], lastword)
                	address['street']=tag.attrib['v']
                elif tag.attrib['k']=="addr:city":
                    address['city']=tag.attrib['v']
                elif tag.attrib['k']=='addr:housenumber':
                    address['housenumber']=tag.attrib['v']
                elif tag.attrib['k']=='addr:postcode':
                	if dashzip.match(tag.attrib['v']):
                		zip=tag.attrib['v'].split('-')[0]
                		tag.attrib['v']=zip
                	address['postcode']=tag.attrib['v']
                elif tag.attrib['k']=='addr:state':
                    address['state']=tag.attrib['v']
                elif tag.attrib['k']=='addr:country':
                    address['country']=tag.attrib['v']
                elif tag.attrib['k']=='addr:unit':
                	address['unit']=tag.attrib['v']
                elif tag.attrib['k']=='addr:suite':
                	address['unit']=tag.attrib['v']
                elif tag.attrib['k']=='building:height':
                	building['height']=tag.attrib['v']
                elif tag.attrib['k']=='building:levels':
                	building['levels']=tag.attrib['v']
                elif tag.attrib['k']=='building:material':
                	building['material']=tag.attrib['v']
                elif tag.attrib['k']=='building:min_level':
                	building['min_level']=tag.attrib['v']           
                elif tag.attrib['k']=='building:use':
                	building['use']=tag.attrib['v']
                elif tag.attrib['k']=='building:color':
                	building['color']=tag.attrib['v']
                elif tag.attrib['k']=='building:colour':
                	building['color']=tag.attrib['v']
              
              
                elif tag.attrib['k']=='lane:backward':
                	building['lane_backward']=tag.attrib['v']
                elif tag.attrib['k']=='lane:bothways':
                	building['lane_bothways']=tag.attrib['v']
                elif tag.attrib['k']=='lane:forward':
                	building['lane_forward']=tag.attrib['v']

                elif tag.attrib['k']=='telescope:diameter':
                	telescope['diameter']=tag.attrib['v']
                elif tag.attrib['k']=='telescope:spectrum':
                	telescope['spectrum']=tag.attrib['v']
                elif tag.attrib['k']=='telescope:type':
                	telescope['type']=tag.attrib['v']
                
                elif tag.attrib['k']=='roof:alignment':
                	roof['alignment']=tag.attrib['v']
                elif tag.attrib['k']=='roof:angle':
                	roof['angle']=tag.attrib['v']
                elif tag.attrib['k']=='roof:color':
                	roof['color']=tag.attrib['v']
                elif tag.attrib['k']=='roof:colour':
                	roof['color']=tag.attrib['v']
                elif tag.attrib['k']=='roof:direction':
                	roof['direction']=tag.attrib['v']
                elif tag.attrib['k']=='roof:height':
                	roof['height']=tag.attrib['v']
                elif tag.attrib['k']=='roof:material':
                	roof['material']=tag.attrib['v']
                elif tag.attrib['k']=='roof:max_height':
                	roof['max_height']=tag.attrib['v']
                elif tag.attrib['k']=='roof:orientation':
                	roof['orientation']=tag.attrib['v']
                elif tag.attrib['k']=='roof:shape':
                	roof['shape']=tag.attrib['v']

                if telescope:
                	node['telescope']=telescope
                if roof:
                	node['roof']=roof
                if building:
					node['building_details']=building
                if address:
                	node['address']=address
        return node
    else:
        return None

#This part is from the lesson
def process_map(file_in):
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
	context=ET.iterparse(filename)
	streettype=dict()
	oddstreetname=set()
	for event, elem in context:
    	 if elem.tag=="node" or elem.tag=="way":
        	for tag in elem.iter("tag"):
            	 if tag.attrib['k']=="addr:street":
                	lastword=tag.attrib['v'].split()[-1]
                	if lastword not in expected:
                    	 oddstreetname.add(tag.attrib['v'])
                	if lastword in streettype:
                    	 streettype[lastword]=streettype[lastword]+1
                	else:
                    	 streettype[lastword]=1
	return streettype, oddstreetname

def updatestreet(street, lastword):
	if lastword in Mapping:
		street=street.replace(lastword, Mapping[lastword])
	return street


def auditzipcode(filename):
	zipcode=dict()
	context=ET.iterparse(filename)
	for event, elem in context:
		if elem.tag=="node" or elem.tag=="way":
			for el in elem.iter("tag"):
				if el.attrib['k']=="addr:postcode":
					if el.attrib['v'] not in zipcode:
						zipcode[el.attrib['v']]=1
					else:
						zipcode[el.attrib['v']]=zipcode[el.attrib['v']]+1
	return zipcode

def audittag(filename):
	tag=dict()
	context=ET.iterparse(filename)
	for event, elem in context:
		if elem.tag=="node" or elem.tag=="way":
			for el in elem.iter("tag"):
				if el.attrib['k'] not in tag:
					tag[el.attrib['k']]=1
				else:
					tag[el.attrib['k']]=tag[el.attrib['k']]+1
	return tag


def main():
	tree="hawaii-latest.osm"
	zip=auditzipcode(tree)
	tag=audittag(tree)
	type, name=audit(tree)
	datajson=process_map(tree)


if __name__=='__main__':
	main()