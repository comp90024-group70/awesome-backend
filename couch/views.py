from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import couchdb
from .common import cors_middleware

COUCHDB_SERVER = 'http://172.26.136.13:5984/'
server = couchdb.Server(COUCHDB_SERVER)
server.resource.credentials = ("admin", "wza7626222")


# Create your views here.
@cors_middleware
@csrf_exempt
def health_check(request):
    response = JsonResponse(
        status=200,
        data={
            'health check': 'OK',
            'database': server.version()
        }
    )
    return response


@cors_middleware
@csrf_exempt
def sentiment_analysis(request: HttpRequest):
    db = server["twitter_clean"]
    view = db.view('design2/view1', group=True)
    res = []
    for row in view:
        res.append(
            {
                "gcc": row["key"],
                "sentiment_avg": round(row["value"][0] / row["value"][1], 5)
            }
        )
    return JsonResponse(
        data={'data': res},
        status=200
    )


@cors_middleware
@csrf_exempt
def get_ado_family(request):
    db = server["ado_fam"]
    view = db.view('design1/view1')
    res = []
    for row in view:
        data = {
            "date": row["key"].split("-", 1)[1],
            "total": row["value"]
        }
        res.append(data)
    return JsonResponse(
        data={'data': res},
        status=200
    )


@cors_middleware
@csrf_exempt
def get_ado_job(request):
    db = server["ado_job"]
    view = db.view('design1/view1')
    res = []
    for row in view:
        data = {
            "date": row["key"].split("-", 1)[1],
            "total": row["value"]
        }
        res.append(data)
    return JsonResponse(
        data={'data': res},
        status=200
    )


@cors_middleware
@csrf_exempt
def get_sa4_family(request):
    db = server["sa4_family"]
    view = db.view('design1/view1')
    res = []
    for row in view:
        res.append(row["key"])
    return JsonResponse(
        data={'data': res},
        status=200
    )


@cors_middleware
@csrf_exempt
def get_sa4_job(request):
    db = server["sa4_job"]
    view = db.view('design1/view1')
    res = []
    for row in view:
        res.append(row["key"])
    return JsonResponse(
        data={'data': res},
        status=200
    )


@cors_middleware
@csrf_exempt
def get_twitter_topics(request: HttpRequest):
    # get query params
    topic = request.GET.get('topic')
    if topic == "cov":
        db = server["twitter_topic_cov"]
    elif topic == "fam":
        db = server["twitter_topic_fam"]
    elif topic == "job":
        db = server["twitter_topic_job"]
    else:
        return JsonResponse(
            data={'data': []},
            status=200
        )
    view = db.view('design1/view1')
    res = []
    for row in view:
        res.append(row["key"])
    return JsonResponse(
        data={'data': res},
        status=200
    )
