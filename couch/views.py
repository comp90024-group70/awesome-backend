from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import couchdb

COUCHDB_SERVER = 'http://admin:wza7626222@demo-couchdb:5984'


# Create your views here.
@csrf_exempt
def health_check(request):
    return JsonResponse(
        status=200,
        data={
            'health check': 'OK'
        }
    )


@csrf_exempt
def check_database_connection(request: HttpRequest):
    # connect to couchdb
    couch = couchdb.Server(url=COUCHDB_SERVER)
    couch.resource.credentials = ("admin", "wza7626222")
    # create a database
    db = couch.create('couch_demo')
    response = JsonResponse({'status': 'ok'})
    return response
