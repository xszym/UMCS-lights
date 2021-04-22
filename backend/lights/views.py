from django.http import JsonResponse
import redis


redis_db = redis.Redis(host='redis', port=6379)


def getDMXvalues(request):
    dmx_values = redis_db.get("DMXvalues").decode('utf-8')
    data = {"DMXvalues": dmx_values}
    return JsonResponse(data)


def ping(request):
    data = {"ping": "pong!"}
    return JsonResponse(data)
    