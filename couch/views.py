from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import couchdb
from .common import cors_middleware
import os

COUCHDB_DOMAIN = os.environ.get("COUCHDB_DOMAIN", "172.26.131.154")
COUCHDB_USER = os.environ.get("COUCHDB_USER", "admin")
COUCHDB_PASSWORD = os.environ.get("COUCHDB_PASSWORD", "wza7626222")
COUCHDB_SERVER = f'http://{COUCHDB_DOMAIN}:5984'
server = couchdb.Server(COUCHDB_SERVER)
server.resource.credentials = (COUCHDB_USER, COUCHDB_PASSWORD)


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
    views = {
        "disability_support": db.view('design1/disability-support', group=True),
        "family_tax_benefit": db.view('design1/family-tax-benefit', group=True),
        "rent_assistant": db.view('design1/rent-assistant', group=True),
        "youth_allowance": db.view('design1/youth-allowance', group=True),
    }
    res = {}
    for view_name, view in views.items():
        res[view_name] = {}
        for row in view:
            res[view_name][row["key"]] = round(row["value"][0] / row["value"][1], 6)
    view_keys = list(views.keys())
    new = {
        "brisbane": {k: res[k]["brisbane"] for k in view_keys},
        "perth": {k: res[k]["perth"] for k in view_keys},
        "sydney": {k: res[k]["sydney"] for k in view_keys},
        "melbourne": {k: res[k]["melbourne"] for k in view_keys},
    }
    return JsonResponse(
        data={'data': new},
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


@cors_middleware
@csrf_exempt
def get_mas(request: HttpRequest):
    db = server["mastodon"]
    # 定义map函数
    design_doc_id = '_design/design1'
    if design_doc_id in db and 'view1' in db[design_doc_id]['views']:
        pass
    else:
        map_func = '''function(doc) {
          if(doc.created_at) {
            emit(doc.created_at, doc);
          }
        }'''
        # 创建设计文档
        design_doc = {
            "_id": "_design/design1",
            "views": {
                "view1": {
                    "map": map_func
                }
            }
        }
        # 保存设计文档到数据库
        db.save(design_doc)
    result = db.view("design1/view1", descending=True, limit=1)
    # 获取最后一条记录
    latest_document = result.rows[0].value
    return JsonResponse(
        data={'data': latest_document},
        status=200
    )


@cors_middleware
@csrf_exempt
def twitter_count(request: HttpRequest):
    db = server["twitter_clean"]
    view = db.view('design2/view2')
    res = {"count": 0}
    for row in view:
        res["count"] += row["value"]
    return JsonResponse(
        data={'data': res},
        status=200
    )


@cors_middleware
@csrf_exempt
def mastodon_count(request: HttpRequest):
    db = server["mastodon"]
    design_doc_id = '_design/design2'
    if design_doc_id in db and 'view2' in db[design_doc_id]['views']:
        pass
    else:
        map_func = '''function(doc) {
            emit(doc._id, 1);
        }'''
        design_doc = {
            "_id": "_design/design2",
            "views": {
                "view2": {
                    "map": map_func,
                    'reduce': '_count'
                }
            }
        }
        # 保存设计文档到数据库

        db.save(design_doc)
    view = db.view('design2/view2')
    res = {"count": 0}
    for row in view:
        res["count"] += row["value"]
    return JsonResponse(
        data={'data': res},
        status=200
    )
