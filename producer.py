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
parser.add_argument("-t", "--type", type=str, help="Queue Type: classic/quorum default is classic", default="classic")
parser.add_argument("-d", "--durable", type=str, help="Queue durable: true/false default is true", default="true")
parser.add_argument("-u", "--username", type=str, help="username, default is guest", default="guest")
parser.add_argument("-p", "--password", type=str, help="password, default is guest", default="guest")
parser.add_argument("-v", "--virtualhost", type=str, help="Virtualhost,  default is /", default="/")

# parse arguments
args = parser.parse_args()
Message = args.message
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
  channel.basic_publish(exchange='', routing_key=Queue, body=Message)
  print("[] Message: \"" +Message+ "\" send to RabbitMQ")
  connection.close()

if __name__ == '__main__':

  try:
    main()

  except pika.exceptions.AMQPConnectionError:
      print('Connection Error to RabbitMQ !')

  except pika.exceptions.ChannelClosedByBroker:
      print('Check your queue x-queue-type value anche set classic|quorum by -t or --type argument')

  except :
      print('Something went wrong !')
