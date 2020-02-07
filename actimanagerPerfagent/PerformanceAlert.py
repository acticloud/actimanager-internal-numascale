from flask_restful import Resource, reqparse
from flask import request

performancealerts = [
    {
        "id": "1",
        "status": 0
    }
]

class PerformanceAlert(Resource):

    def get(self, id):
        for performancealert in performancealerts:
            if (id == performancealert["id"]):
                return performancealert, 200
        return "AppID not found", 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("status")
        args = parser.parse_args()


        for performancealert in performancealerts:
            if (id == performancealert["id"]):
                performancealert["status"] = args["status"]
                print "Performance alert received! IP: " + str(request.remote_addr) + " domainID: " + id + " status: " + performancealert["status"]
                return performancealert, 200

        return "AppID not found", 404
