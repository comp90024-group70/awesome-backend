import couchdb
from couchdb.design import ViewDefinition
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .common import cors_middleware

COUCHDB_SERVER = 'http://admin:wza7626222@demo-couchdb:5984'
# COUCH_SERVER = 'http://127.0.0.1:5984'
# COUCHDB_SERVER = 'http://172.26.136.13:5984/'
server = couchdb.Server(COUCHDB_SERVER)
server.resource.credentials = ("admin", "wza7626222")


@csrf_exempt
@cors_middleware
def sentiment_analysis(request: HttpRequest):
    db = server["twitter_clean"]
    view = db.view('design1/view1')
    res = []
    for row in view:
        res.append(row["value"])
    return JsonResponse(
        data={'data': res},
        status=200
    )
