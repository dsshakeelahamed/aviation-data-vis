from flask import Flask, Response, request
from flask_cors import CORS
from flask_restful import Api, Resource
from db_module import MongoDBModule
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

db_module = MongoDBModule()


class AviationAccidents(Resource):
    def get(self):
        data, status_code = db_module.get_aviation_accidents()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AviationDestroyed(Resource):
    def get(self):
        data, status_code = db_module.get_aircraft_destroyed()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AviationFatalInjuries(Resource):
    def get(self):
        data, status_code = db_module.get_fatal_injuries()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AviationSeriousInjuries(Resource):
    def get(self):
        data, status_code = db_module.get_serious_injuries()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AviationLineGraph(Resource):
    def get(self):
        data, status_code = db_module.get_line_graph_data()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AviationBarGraph(Resource):
    def get(self):
        data, status_code = db_module.get_bar_graph_data()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AviationPieChart(Resource):
    def get(self):
        data, status_code = db_module.get_pie_chart_data()
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AviationAllData(Resource):
    def get(self):
        # get data and parse according to required fields
        data, status_code = db_module.get_all_data(request.args.get('page_size', 8), request.args.get('page_num', 1))
        response = Response(json.dumps(data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    def post(self):
        data = request.get_json()
        response_data, status_code = db_module.create_record(data)
        response = Response(json.dumps(response_data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response_data, status_code

    # def delete(self):
    #     print(request.args)
    #     response_data, status_code = db_module.delete_record(request.args.get('id', None))
    #     response = Response(json.dumps(response_data), status_code, content_type="Application/Json")
    #     response.headers.add("Access-Control-Allow-Origin", "*")
    #     return response_data, status_code


class AviationDelete(Resource):
    def delete(self, id):
        response_data, status_code = db_module.delete_record(id)
        response = Response(json.dumps(response_data), status_code, content_type="Application/Json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response_data, status_code


api.add_resource(AviationAccidents, "/aviation/accidents")
api.add_resource(AviationDestroyed, "/aviation/destroyed")
api.add_resource(AviationFatalInjuries, "/aviation/fatal")
api.add_resource(AviationSeriousInjuries, "/aviation/serious")
api.add_resource(AviationLineGraph, "/aviation/line")
api.add_resource(AviationBarGraph, "/aviation/bar")
api.add_resource(AviationPieChart, "/aviation/pie")
api.add_resource(AviationAllData, "/aviation/data")
api.add_resource(AviationDelete, "/aviation/data/<id>")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8081)
