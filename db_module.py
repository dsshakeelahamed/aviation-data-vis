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
            accident_count = []
            accident_year = []
            for record in response:
                accident_count.append(record.get("TotalAccidents", 0))
                accident_year.append(str(record.get("year", "NA")))
            output_json = {"line_chart_data": [{"data": accident_count, "label": "TotalAccidents"}],
                           "line_chart_labels": accident_year}
            return output_json, 200
        except Exception as e:
            # print(e)
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def get_bar_graph_data(self):
        try:
            response = self.collection.aggregate(query.bar_graph)
            output = []
            for record in response:
                record['data'] = [record.get('data')]
                output.append(record)
            output_json = {"bar_chart_data": output}
            return output_json, 200
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

    def get_all_data(self, page_size, page_num):
        try:
            page_size = int(page_size)
            page_num = int(page_num)
            if page_size <= 0:
                page_size = 1
            if page_num <= 0:
                page_num = 10
            record_start = (page_size * (page_num - 1))
            all_data = self.collection.find({}, {"_id": 0, "Event": 1, "Location" : 1, "Injury": 1, "Aircraft": 1, "Make": 1,
                                                 "Total": 1, "Weather": 1, "Broad": 1, "FAR": 1}).skip(record_start).limit(page_size)
            output = []
            for data in all_data:
                record = {}
                record['EventId'] = data.get('Event', {}).get('Id', 0)
                record['EventDate'] = data.get('Event', {}).get('Date', '1970-01-01')
                record['Location'] = data.get('Location', "NA")
                record['InjurySeverity'] = data.get('Injury', {}).get('Severity', 'NA')
                record['AircraftDamage'] = data.get('Aircraft', {}).get('damage', 'NA')
                record['Make'] = data.get('Make', 'NA')
                record['TotalFatalInjuries'] = data.get('Total', {}).get('Fatal', {}).get('Injuries', 0)
                record['TotalSeriousInjuries'] = data.get('Total', {}).get('Serious', {}).get('Injuries', 0)
                record['WeatherCondition'] = data.get('Weather', {}).get('Condition', 'NA')
                record['Broadphaseofflight'] = data.get('Broad', {}).get('phase', {}).get('of', {}).get('flight', 'NA')
                record['Description'] = data.get('FAR', {}).get('Description', 'NA')
                output.append(record)

            return {'data': output}, 200
        except Exception as e:
            print(e)
            print("Error while fetching records, Try again")
            return {"Error": "Couldn't fetch records, please try later"}, 400

    def create_record(self, data):
        try:
            # break the input data and build the json to be inserted
            data_json = {
                "Event": {
                    "Id": data.get("EventId", "NA"),
                    "Date": data.get("EventDate", "NA")
                },
                "Location": data.get("Location", "NA"),
                "FAR": {
                    "Description": data.get("Description", "NA")
                },
                "Injury": {
                    "Severity": data.get("InjurySeverity", "NA")
                },
                "Aircraft": {"Damage": data.get("AircraftDamage", "NA")},
                "Total": {"Fatal": {"Injuries": data.get("TotalFatalInjuries", "NA")}}
            }
            print(data_json)
            self.collection.insert_one(data_json)
            return {"message": "Successfully inserted record"}, 200
        except Exception as e:
            print(e)
            print("Error while inserting record, Try again")
            return {"Error": "Error while inserting record, please try later"}, 400

    def delete_record(self, id):
        try:
            if id:
                self.collection.delete_one({"Event.Id": str(id)})
                return {"message": "Successfully deleted record"}, 200
            else:
                return {"message": "Invalid Id"}, 200
        except Exception as e:
            print(e)
            print("Error while deleting record, Try again")
            return {"Error": "Error while deleting record, please try later"}, 400

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
