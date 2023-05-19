from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import couchdb
from .common import cors_middleware

COUCHDB_SERVER = 'http://admin:wza7626222@demo-couchdb:5984'
server = couchdb.Server(COUCHDB_SERVER)
# server.resource.credentials = ("admin", "wza7626222")


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
            data={'data': {}},
            status=200
        )
    # db = server["twitter_topic_cov_test"]
    view = db.view('design1/view1', group=True)
    res = {}
    for row in view:
        key = row["key"]
        count = row["value"]
        gcc, sentiment = key
        if not res.get(gcc):
            res[gcc] = {}
        if not res[gcc].get(sentiment):
            res[gcc][sentiment] = 0
        res[gcc][sentiment] += count
    return JsonResponse(
        data={'data': res},
        status=200
    )


@cors_middleware
@csrf_exempt
def get_treemap(request: HttpRequest):
    db = server["twitter_treemaps"]
    view = db.view('design1/view1')
    res = {}
    for row in view:
        res[row["key"]] = row["value"]
    return JsonResponse(
        data={'data': res},
        status=200
    )
