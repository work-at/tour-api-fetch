import redis
import json

r = redis.StrictRedis(
    host='34.64.37.69',
    port=6379,
    charset="utf-8",
    decode_responses=True,
    password='workat@1234'
)

for key in r.keys("yearly:*"):
    visitor = r.hgetall(key)
    id = visitor['id']
    elements = r.lrange(id, 0, 364)
    avg = 0.0
    for pair in elements:
        result = json.loads(pair)
        avg += sum(result.values())
    avg = avg / len(elements)
    visitor['count'] = str(avg)
    r.hset(key, mapping=visitor)


for key in r.keys("monthly:*"):
    visitor = r.hgetall(key)
    id = visitor['id']
    elements = r.lrange(id, 0, 30)
    avg = 0.0
    for pair in elements:
        result = json.loads(pair)
        avg += sum(result.values())
    avg = avg / len(elements)
    visitor['count'] = str(avg)
    r.hset(key, mapping=visitor)
