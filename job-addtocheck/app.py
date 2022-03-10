import json
import os
import redis


REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASS = os.getenv('REDIS_PASS')


def main():
    with open('services_to_check.json') as f:
        services_obj = json.load(f)
    
    r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASS)

    for service in services_obj:
        service_hostname = service.get('server')
        r.set(service_hostname, json.dumps(service))


if __name__ == "__main__":
    main()