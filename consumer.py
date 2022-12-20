#!/usr/bin/python

import pika
import argparse
import sys
import os
import time

# Declare arguments
parser = argparse.ArgumentParser(description='RabbitMQ Arguments')
parser.add_argument("-r", "--rabbithost", type=str, help="RabbitMQ host ex: 127.0.0.1", required=True)
parser.add_argument("-q", "--queue", type=str, help="Name of RabbitMQ queue ex: QUEUE01", required=True)
parser.add_argument("-t", "--type", type=str, help="Queue Type: classic/quorum default is classic", default="classic")
parser.add_argument("-d", "--durable", type=str, help="Queue durable: true/false default is true", default="true")
parser.add_argument("-u", "--username", type=str, help="username, default is guest", default="guest")
parser.add_argument("-p", "--password", type=str, help="password, default is guest", default="guest")
parser.add_argument("-v", "--virtualhost", type=str, help="Virtualhost,  default is /", default="/")

# Parse arguments
args = parser.parse_args()
Rabbit_host = args.rabbithost
Queue = args.queue
Type = args.type
Durable = args.durable
Username = args.username
Password = args.password
Vhost = args.virtualhost

# credentials
credentials = pika.PlainCredentials(Username, Password)

# main function
def main():
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=Rabbit_host, port='5672',virtual_host=Vhost, credentials=credentials))
  channel = connection.channel()
  channel.queue_declare(queue=Queue, durable=Durable, arguments={'x-queue-type' : Type})
  print(' [ ] Waiting messages. type CTRL+C for exit')

  #callback function
  def callback(ch, method, properties, body):
      print(" [] Received %r" % body.decode())
      time.sleep(body.count(b'.'))
      print(" [] Done")
      ch.basic_ack(delivery_tag=method.delivery_tag)

  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(queue=Queue, on_message_callback=callback)
  channel.start_consuming()    

if __name__ == '__main__':

  try:
    main()

  except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

