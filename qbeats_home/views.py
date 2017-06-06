
from django.shortcuts import render, render_to_response
from django.core import management

def qbeats_home(request):

    return render_to_response('qbeats_home/index.html')