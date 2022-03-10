import json
import os
import pika
import redis
import time


REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASS = os.getenv('REDIS_PASS')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RMQ_QUEUE = os.getenv('RMQ_QUEUE')


def main():
    while True:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASS)
        
        runs = 0
        for key in r.scan_iter("*"):
            runs += 1

            target = r.get(key)

            rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            rmq_channel = rmq.channel()
            rmq_channel.queue_declare(queue=RMQ_QUEUE)
            rmq_channel.basic_publish(exchange='', routing_key=RMQ_QUEUE, body=target)
            rmq.close()
        
        if runs == 0:
            time.sleep(1)
        else:
            time.sleep(5)


if __name__ == "__main__":
    main()