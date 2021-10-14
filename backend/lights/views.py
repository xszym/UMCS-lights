import os
import redis

from django.http import JsonResponse
from django.shortcuts import render


redis_db = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=int(os.environ['REDIS_PORT'])
)


def getDMXvalues(request):
    dmx_values = redis_db.get('DMXvalues').decode('utf-8')
    data = {'DMXvalues': dmx_values}
    return JsonResponse(data)


def ping(request):
    data = {'ping': 'pong!'}
    return JsonResponse(data)

def home(request):
    return render(request, 'lights/home.html')
