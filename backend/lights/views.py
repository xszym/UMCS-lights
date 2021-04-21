from django.http import JsonResponse
import redis


redis_db = redis.Redis(host='redis', port=6379)


def ping(request):
    DMXvalues = redis_db.get("DMXvalues").decode('utf-8')
    data = {"DMXvalues": DMXvalues}
    return JsonResponse(data)
