from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import couchdb

COUCHDB_SERVER = 'http://admin:wza7626222@demo-couchdb:5984'


# Create your views here.
@csrf_exempt
def health_check(request):
    response = JsonResponse(
        status=200,
        data={
            'health check': 'OK'
        }
    )
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'content'
    return response


@csrf_exempt
def check_database_connection(request: HttpRequest):
    # connect to couchdb
    couch = couchdb.Server(url=COUCHDB_SERVER)
    couch.resource.credentials = ("admin", "wza7626222")
    response = JsonResponse({'status': 'ok'})
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'content'
    return response
