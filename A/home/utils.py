import redis
from django.conf import settings

redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0
)
