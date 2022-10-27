import json
import os
str = [
    b'{"_id": "634e29dad26cebaa2878fffd",\
    "Name": "Maguire", "lastName": "Harry"}'
    ]
redis_host = os.environ.get('REDIS_HOST', 'localhost')
print(redis_host)
