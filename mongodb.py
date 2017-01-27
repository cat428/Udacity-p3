from pymongo import MongoClient
import pprint

client = MongoClient('localhost')
db=client.test

def zipcode():
	numbers=db.opens.find({"address.postcode":{"$exists":1}}).count()
	result=db.opens.aggregate([{"$match":{"address.postcode":{"$exists":1}}}, {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, {"$sort":{"count":1}}])
	return numbers, result

def modifyzipcode():
	db.opens.update({"address.postcode":"2750"}, {"$unset":{"address.postcode":""}}, multi=True)
	db.opens.update({"address.postcode":{"$regex":"HI"}}, {"$unset":{"address.postcode":""}}, multi=True)

def uniqueusers():
	num=db.opens.find({"created.user":{"$exists":1}}).count()
	most=db.opens.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":1}}])
	users=db.opens.distinct("created.user")
	return num, most, users

def restaurants():
	restaurants=db.opens.aggregate([{"$match":{"amenity":"restaurant", "address.postcode":{"$exists":1}}}, {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, {"$sort":{"count":1}}])
	return restaurants

def restauranttype():
	number=db.opens.find({"amenity":"restaurant"}).count()
	restaurants=db.opens.aggregate([{"$match":{"amenity":"restaurant", "cuisine":{"$exists":1}}}, {"$group":{"_id":"$cuisine", "count":{"$sum":1}}}, {"$sort":{"count":1}}])
	return number, restaurants
def material():
	num=db.opens.find({"building_details.color":{"$exists":1}}).count()
	mat=db.opens.aggregate([{"$match":{"building_details.color":{"$exists":1}}}, {"$group":{"_id":"$building_details.color", "count":{"$sum":1}}}])
	return num, mat

def main():
	modifyzipcode()
	numz, result=zipcode()
	num, most, users=uniqueusers()
	numberr=restaurants()
	numr, type=restauranttype()
	n, mat=material()
	print n
	print len(users)
	for a in mat:
		print a

if __name__=='__main__':
	main()