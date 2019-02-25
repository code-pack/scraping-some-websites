import pymongo
import json

def write_to_db(input):
    
    try:
        # setup mongo connection
        conn = "mongodb://localhost:27017"
        myclient = pymongo.MongoClient(conn)

        mydb = myclient["mars"]

        mycol = mydb["weather"]

        x = mycol.delete_many({})
        print(x.deleted_count, " documents deleted.")

        #print(input)
        x = mycol.insert_one(input)

        #print list of the _id values of the inserted documents:
        #print(x.inserted_id)

        for x in mycol.find():
            print(x)
        
        return 0
    except Exception as e:
        print(e)
        return -1


def read_DB():

    output = {}
    
    try:
        # setup mongo connection
        conn = "mongodb://localhost:27017"
        myclient = pymongo.MongoClient(conn)

        mydb = myclient["mars"]

        mycol = mydb["weather"]

        output_list = []

        for x in mycol.find({},{ "_id": 0}):
            output_list.append(x)

        output = output_list[0]

        
    except Exception as e:
        print(e)
  
    return output
