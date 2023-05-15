import couchdb
from couchdb.design import ViewDefinition
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

# COUCHDB_SERVER = 'http://admin:wza7626222@demo-couchdb:5984'
# COUCH_SERVER = 'http://127.0.0.1:5984'
COUCHDB_SERVER = 'http://172.26.136.13:5984/'
server = couchdb.Server(COUCHDB_SERVER)
server.resource.credentials = ("admin", "wza7626222")


@csrf_exempt
def count_docs(request: HttpRequest):
    """返回mastodon中文档的数量，并且实时更新"""
    db = server["twitter"]
    map_fun = '''function(doc) {
      emit(doc._id, 1);
    }'''

    # 定义你的reduce函数
    reduce_fun = '''function(keys, values, rereduce) {
      return sum(values);
    }'''
    view = ViewDefinition('twitter_count', 'count_by_id', map_fun, reduce_fun=reduce_fun)

    # 将view保存到数据库中
    view.sync(db)

    res = {}
    # 使用view
    for row in db.view('twitter_count/count_by_id'):
        key = row.key
        value = row.value
        res[key] = value
    response = JsonResponse(
        status=200,
        data=res
    )
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'content'
    return response


@csrf_exempt
def get_sentiment_by_state(request: HttpRequest):
    db = server["twitter_clean"]
    map_fun = '''function(doc) {
      emit(doc.sentiment, doc.gcc, 1);
    }'''
    reduce_fun = '''function(keys, values, rereduce) {
      return values;
    }'''
    view = ViewDefinition('sentiment_by_state_view', 'sentiment_by_state', map_fun, reduce_fun=reduce_fun)
    # 将view保存到数据库中
    view.sync(db)
    res = {
        "data": [
            {"sydney": 0.67},
            {"melbourne": -0.9},
            {"perth": 0.8}
        ]
    }
    # # 使用view
    # for row in db.view('sentiment_by_state_view/sentiment_by_state'):
    #     key = row.key
    #     value = row.value
    #     res[key] = value
    #     # print(row)
    response = JsonResponse(
        status=200,
        data=res,
    )
    """
    {"total":{"country":["synde","melbourne"]},
    """
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'content'
    return response
