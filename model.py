from bson import json_util
from mongoengine import *
import datetime

class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class DepartmentReview(Document):
    stars = IntField()
    comment = StringField()
    author = ObjectIdField()
    department = IntField()
    created_when = DateTimeField(default=datetime.datetime.now())
    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(self.id)
        data['author'] = str(self.author)
        return json_util.dumps(data)


class ChairRating(EmbeddedDocument):
    teachers = IntField(default=0)
    course = IntField(default=0)
    facility = IntField(default=0)
    communication = IntField(default=0)


class ChairReview(Document):
    comment = StringField()
    author = ObjectIdField()
    chair = IntField()
    rating = EmbeddedDocumentField(ChairRating)
    created_when = DateTimeField()

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(self.id)
        data['author'] = str(self.author)
        return json_util.dumps(data)