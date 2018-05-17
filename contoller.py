from werkzeug.exceptions import NotFound

from model import *


def add_review(review_json):
    review = DepartmentReview(**review_json)
    review.created_when = datetime.datetime.now()
    review.save()
    return {'review_id': str(review.id)}

def add_chair_review(review_json):
    review = ChairReview(**review_json)
    review.created_when = datetime.datetime.now()
    review.save()
    return {'review_id': str(review.id)}

def update_review(review_id, review_json):
    review = DepartmentReview.objects(id=review_id)
    return review.update(**review_json)


def delete_review(review_id):
    review = DepartmentReview.objects(id=review_id).first()
    if review is not None:
        deleted = review.delete()
        print(deleted)
        return deleted
    else:
        raise NotFound


def get_review(_id):
    return DepartmentReview.objects(id=_id).first()


def get_all_review(l=10, s=0):
    reviews = DepartmentReview.objects.skip(s).limit(l)
    return reviews


def get_dep_review_report():
    pipeline = [{"$group": {'_id': '$department', 'stars': {'$avg': '$stars'}}},{"$sort":{"stars":-1}}]
    reviews = DepartmentReview.objects.aggregate(*pipeline)
    return list(reviews)


def get_review_department(_id, l=10, s=0):
    reviews = DepartmentReview.objects(department=_id).order_by('created_when').skip(s).limit(l)
    return reviews


def get_review_chair(_id, l=10, s=0):
    reviews = ChairReview.objects(chair=_id).order_by('-created_when').skip(s).limit(l)
    return reviews


def get_avg_department(_id):
    avg = DepartmentReview.objects(department=_id).average('stars')
    return avg


def get_avg_chair(_id):
    chairs = ChairReview.objects(chair=_id)

    average = (chairs.average('rating.teachers') +
               chairs.average('rating.course') +
               chairs.average('rating.facility') +
               chairs.average('rating.communication'))/4
    return average