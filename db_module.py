from pymongo import MongoClient
import pandas as pd
import json
import queries as query
import config as cfg


class MongoDBModule:
    def __init__(self) -> None:
        self.client = MongoClient("mongodb+srv://%s:%s@cluster0.tkpjd.mongodb.net" % (cfg.username, cfg.password))
        self.db = self.client.myFirstDatabase
        self.collection = self.db.aviation_data
        pass

    def import_csv(self, file_location):
        data = pd.read_csv(file_location, encoding='cp1252')
        data = json.loads(data.to_json(orient='records'))
        db = self.client.test_db
        collection = db.test_collection
        collection.insert_many(data)
        print("Success")


    def get_aviation_accidents(self):
        try:
            response = self.collection.aggregate(query.aviation_accidents)
            for record in response:
                return record, 200
        except Exception as e:
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def get_aircraft_destroyed(self):
        try:
            response = self.collection.aggregate(query.aircrafts_destroyed)
            for record in response:
                # print(record.get("num_accidents", 0))
                return record, 200
            # print(response)
        except Exception as e:
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def get_fatal_injuries(self):
        try:
            response = self.collection.aggregate(query.fatal_injuries)
            for record in response:
                return record, 200
        except Exception as e:
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def get_serious_injuries(self):
        try:
            response = self.collection.aggregate(query.serious_injuries)

            for record in response:
                return record, 200
        except Exception as e:
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def get_line_graph_data(self):
        try:
            response = self.collection.aggregate(query.line_graph)
            output = []
            for record in response:
                output.append(record)
            return output, 200
        except Exception as e:
            # print(e)
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def get_bar_graph_data(self):
        try:
            response = self.collection.aggregate(query.bar_graph)
            output = []
            for record in response:
                output.append(record)
            return output, 200
        except Exception as e:
            print(e)
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def get_pie_chart_data(self):
        try:
            fatal_accidents = self.collection.aggregate(query.fatal_accidents)
            output = {}
            for record in fatal_accidents:
                output.update(record)

            nonfatal_accidents = self.collection.aggregate(query.non_fatal_accidents)
            for record in nonfatal_accidents:
                output.update(record)
            return output, 200
        except Exception as e:
            print(e)
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400



if __name__ == "__main__":
    obj = MongoDBModule()
    # obj.import_csv("/Users/shakeelahamed/Documents/Sem_2/ADT/project/archive/AviationData.csv")
    # obj.get_aviation_accidents()
    # print(obj.get_aviation_accidents())
    # print(obj.get_aircraft_destroyed())
    # print(obj.get_fatal_injuries())
    # print(obj.get_serious_injuries())
    # print(obj.get_line_graph_data())
    # print(obj.get_bar_graph_data())
