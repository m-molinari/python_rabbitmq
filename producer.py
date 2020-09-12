#!/usr/bin/python

# import modules
import pika
import sys
import argparse

# declare arguments
parser = argparse.ArgumentParser(description='RabbitMQ Arguments')
parser.add_argument("-r", "--rabbithost", type=str, help="RabbitMQ host ex: 127.0.0.1", default="localhost")
parser.add_argument("-m", "--message", type=str, help="body of message (need quotes if there are spaces), ex : \"hello world\"", default="Body Messagge Example")
parser.add_argument("-q", "--queue", type=str, help="Name of RabbitMQ queue ex: QUEUE01", required=True)

# parse arguments
args = parser.parse_args()
Message = args.message
Rabbit_host = args.rabbithost
Queue = args.queue

# main function
# TODO manage quorum queue type
# pika.exceptions.ChannelClosedByBroker: (406, "PRECONDITION_FAILED - inequivalent arg 'x-queue-type' for queue 'QUEUEQUORUM01' in vhost '/': received none but current is the value 'quorum' of type 'longstr'")

def main():
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=Rabbit_host))
  channel = connection.channel()
  channel.queue_declare(queue=Queue, durable='true')
  channel.basic_publish(exchange='', routing_key=Queue, body=Message)
  print("[] Message: \"" +Message+ "\" send to RabbitMQ")
  connection.close()

if __name__ == '__main__':

  try:
    main()

  except pika.exceptions.AMQPConnectionError:
      print('Connection Error to RabbitMQ !')

  except :
      print('Something went wrong !')

