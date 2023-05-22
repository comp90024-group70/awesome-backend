import couchdb
import os

COUCHDB_DOMAIN = os.environ.get("COUCHDB_DOMAIN", "172.26.131.154")
COUCHDB_USER = os.environ.get("COUCHDB_USER", "admin")
COUCHDB_PASSWORD = os.environ.get("COUCHDB_PASSWORD", "wza7626222")
COUCHDB_SERVER = f'http://{COUCHDB_DOMAIN}:5984'
server = couchdb.Server(COUCHDB_SERVER)
server.resource.credentials = (COUCHDB_USER, COUCHDB_PASSWORD)

if "mastodon" in server:
    del server['mastodon']
db = server.create("mastodon")
db = server["mastodon"]
design_doc_id = '_design/design1'

design_doc = {
    "_id": design_doc_id,
    "views": {
        "view1": {
            "map": '''function(doc) {
                if(doc.created_at) {
                    emit(doc.created_at, doc);
                }
            }'''
        },
        'view2': {
            "map": '''function(doc) {
                emit(doc._id, 1);
            }''',
            'reduce': '_count'
        }
    }
}
# 保存设计文档到数据库
db.save(design_doc)
