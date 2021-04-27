from django.http import JsonResponse
import redis
import os


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
