import json
import os
import paramiko
import pika
import time


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RMQ_QUEUE = os.getenv('RMQ_QUEUE')


def connect_and_execute(server, username, password, cmd_to_execute):
    ssh = paramiko.SSHClient()
    ssh.connect(server, username=username, password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)


def main():
    rmq = None
    try:
        rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    except:
        time.sleep(5)
        rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

    rmq_channel = rmq.channel()
    rmq_channel.queue_declare(queue=RMQ_QUEUE)

    def callback(ch, method, properties, body):
        target_data = json.loads(body)
        server = target_data.get('server')
        username = target_data.get('username')
        password = target_data.get('password')
        command = target_data.get('command')

        # try, except ConnectionFailure, except (generic)
        try:
            connect_and_execute(server, username, password, command)
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("Could not connect")

    rmq_channel.basic_consume(queue=RMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    rmq_channel.start_consuming()


if __name__ == "__main__":
    main()