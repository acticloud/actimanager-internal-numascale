#!/usr/bin/env python2
from flask import Flask
from PerformanceAlert import PerformanceAlert
from flask_restful import Api

#start the rest interface for performance alerts
print "**** Performance Alert starting ****"
app = Flask("AM Performance Alerter Service")
api = Api(app)
api.add_resource(PerformanceAlert, "/performancealert/<string:id>")

app.run(debug=True, host='0.0.0.0')