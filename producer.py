#! /usr/bin/env python3

import pika
import sys
import argparse, getpass
import socket

# Declare arguments
parser = argparse.ArgumentParser(description='RabbitMQ Arguments')
parser.add_argument("-r", "--rabbithost", type=str, help="RabbitMQ host ex: 127.0.0.1", default="localhost")
parser.add_argument("-m", "--message", type=str, help="body of message (need quotes if there are spaces), ex : \"hello world\"", default="Body Messagge Example")
parser.add_argument("-q", "--queue", type=str, help="Name of RabbitMQ queue ex: QUEUE01", required=True)
parser.add_argument("-t", "--type", type=str, help="Queue Type: classic/quorum default is classic", default="classic")
parser.add_argument("-d", "--durable", type=str, help="Queue durable: true/false default is true", default="true")
parser.add_argument("-u", "--username", type=str, help="username, default is guest", default="guest")
parser.add_argument("-p", "--password", type=str, help="password, default is guest", nargs='?', const='', default="guest")
parser.add_argument("-v", "--virtualhost", type=str, help="Virtualhost,  default is /", default="/")
parser.add_argument("-n", "--numbers", type=int, help="Loop number of messages", default=1)
parser.add_argument

# Parse arguments
args = parser.parse_args()
Message = args.message
Rabbit_host = args.rabbithost
Queue = args.queue
Type = args.type
Durable = args.durable
Username = args.username
Password = args.password
Vhost = args.virtualhost
Numbers = args.numbers

# Check for remote host connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
result = sock.connect_ex((Rabbit_host,5672))
if result != 0:
  print ("Error to connect to remote Host:", Rabbit_host, "on port: 5672 after 5 seconds, please check it")
  sock.close()
  sys.exit(2)

# If -p args is empty, ask for password
if Password == "":
  Password = getpass.getpass()

credentials = pika.PlainCredentials(Username, Password)

def main():
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=Rabbit_host, port='5672',virtual_host=Vhost, credentials=credentials))
  channel = connection.channel()
  channel.queue_declare(queue=Queue, durable=Durable, arguments={'x-queue-type' : Type})

  # message sending cycle
  for Num in range(1, Numbers+1):
    Message_Num = Message  + " " + str(Num)
    channel.basic_publish(exchange='', routing_key=Queue, body=Message_Num)
    print("[] Message: \""+Message_Num+"" + "\" " "send to RabbitMQ !")
    
  connection.close()

if __name__ == '__main__':

  try:
    main()

  except pika.exceptions.AMQPConnectionError as AMQP_C_E:
      print('Connection Error to RabbitMQ: check authentication data, using "-p" arg for password')
      print(AMQP_C_E)

  except pika.exceptions.ChannelClosedByBroker as AMQP_CCB:
      print('Check your queue x-queue-type value anche set classic|quorum by -t or --type argument')
      print(AMQP_CCB)

  except :
      print('Something went wrong !')
