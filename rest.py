from flask import Flask, Response
from flask_restful import Api, Resource
from db_module import MongoDBModule
import json

app = Flask(__name__)
api = Api(app)

db_module = MongoDBModule()


class AviationAccidents(Resource):
    def get(self):
        data, status_code = db_module.get_aviation_accidents()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        return response


class AviationDestroyed(Resource):
    def get(self):
        data, status_code = db_module.get_aircraft_destroyed()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        return response


class AviationFatalInjuries(Resource):
    def get(self):
        data, status_code = db_module.get_fatal_injuries()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        return response


class AviationSeriousInjuries(Resource):
    def get(self):
        data, status_code = db_module.get_serious_injuries()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        return response


class AviationLineGraph(Resource):
    def get(self):
        data, status_code = db_module.line_graph_data()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        return response


class AviationBarGraph(Resource):
    def get(self):
        data, status_code = db_module.bar_graph_data()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        return response


api.add_resource(AviationAccidents, "/aviation/accidents")
api.add_resource(AviationDestroyed, "/aviation/destroyed")
api.add_resource(AviationFatalInjuries, "/aviation/fatal")
api.add_resource(AviationSeriousInjuries, "/aviation/serious")
api.add_resource(AviationLineGraph, "/aviation/line")
api.add_resource(AviationBarGraph, "/aviation/bar")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8081)
