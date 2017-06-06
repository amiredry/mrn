from django.shortcuts import render, render_to_response, RequestContext
from django.template.loader import render_to_string
from pymongo import MongoClient
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotModified, Http404
from bson.json_util import dumps
from django.contrib.auth.decorators import login_required
from pymongo.errors import ConnectionFailure, PyMongoError
from recaptcha.client import captcha
from django.conf import settings

try:
    connection = MongoClient("server1.ecq3.com", tz_aware=True)  #Create a new connection to a single MongoDB instance at server1.ecq3.com:port=27017.
    db = connection.ecquant
except ConnectionFailure:
    print "ConnectionFailure"

@login_required
def get_apfirst_stories(request):
    """
    Finds and returns the x first AP First documents from the "news" collection.
    """
    try:
        ap_stories = db.news.find({"labels": "apfirst"}, {"header": 1, "created_on": 1, "content": 1, "hash2": 1}).sort("created_on", -1).limit(100)
        return render_to_response('newsfirst/news_first_list_2.html', RequestContext(request,{"news_items": ap_stories }))

    except PyMongoError:
        raise HttpResponseServerError


@login_required
def get_latest_stories(request, hash2=None):
    """
    Finds and returns all documents created after the specified _id value, or returns status code 304 to designate
    that the page hasn't been modified.
    """
    try:
        item = db.news.find_one({"hash2": hash2})
        latest_ap_stories = db.news.find({"labels": "apfirst", "_id": {"$gt": item['_id']}}, {"header": 1, "created_on": 1, "content": 1, "hash2": 1}).sort("created_on", -1)

        if latest_ap_stories.count() == 0:
            return HttpResponseNotModified()
        html = render_to_string('newsfirst/latest_stories.html', {"news_items": latest_ap_stories})

        return HttpResponse(dumps(html))

    except PyMongoError:
        raise HttpResponseServerError


@login_required
def get_story(request, hash2=None):
    """
    Finds and returns a single document, or raise a 404 Not Found
    exception if no document matches the query spec("hash2").
    """
    item = db.news.find_one({"hash2": hash2})
    if item is None:
        raise Http404
    return render_to_response('newsfirst/story_view.html', {"item": item})


def test(request):

    captcha_error = ""
    data = "x"
    if request.method == "POST":

        captcha_response = captcha.submit( request.POST.get("recaptcha_challenge_field", None),request.POST.get("recaptcha_response_field", None),settings.RECAPTCHA_PRIVATE_KEY, request.META.get("REMOTE_ADDR", None))

        if captcha_response.is_valid:
            data = "true"
            return HttpResponse(data)

        else:
            data = captcha_response.error_code
            return HttpResponse(data)


    return render_to_response('newsfirst/test.html', context_instance=RequestContext(request))