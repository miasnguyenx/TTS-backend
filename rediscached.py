import redis


port_number = 6379
host_name = 'redis'


def connect():
    r = redis.Redis(host=host_name, port=port_number, db=0)
    return r

# r.set('foo', 'bar')
# r.get('foo')
# r.set('mykey', 'Hello from Python!')
# value = r.get('mykey')
# print(value)
