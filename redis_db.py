from gzip import READ
from redis import Redis

host_name = '0.0.0.0'
port_number = 6379
db_num = 0


def redis_conn():
    r = Redis(host=host_name, port=port_number, db=db_num)
    return r

# r.set('foo', 'bar')
# r.get('foo')
# r.set('mykey', 'Hello from Python!')
# value = r.get('mykey')
# print(value)
