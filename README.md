# python_rabbitmq

Simple scripts that Produce and Consume messages for RabbitMQ for playing with the Rabbit or stress it :)

## Install
### Clone
```bash
git clone https://github.com/m-molinari/python_rabbitmq.git
```

### Requirements
```bash
pip install -r requirements.txt

```
## Usage
You can use scripts passing args by command line :

### Producer
```bash

usage: producer.py [-h] [-r RABBITHOST] [-m MESSAGE] -q QUEUE [-t TYPE] [-d DURABLE]

RabbitMQ Arguments

optional arguments:
  -h, --help            show this help message and exit
  -r RABBITHOST, --rabbithost RABBITHOST
                        RabbitMQ host ex: 127.0.0.1
  -m MESSAGE, --message MESSAGE
                        body of message (need quotes if there are spaces), ex : "hello world"
  -q QUEUE, --queue QUEUE
                        Name of RabbitMQ queue ex: QUEUE01
  -t TYPE, --type TYPE  Queue Type: classic/quorum
  -d DURABLE, --durable DURABLE
                        Queue durable: true/false


```
### Consumer

```bash
uusage: consumer.py [-h] -r RABBITHOST -q QUEUE [-t TYPE] [-d DURABLE]

RabbitMQ Arguments

optional arguments:
  -h, --help            show this help message and exit
  -r RABBITHOST, --rabbithost RABBITHOST
                        RabbitMQ host ex: 127.0.0.1
  -q QUEUE, --queue QUEUE
                        Name of RabbitMQ queue ex: QUEUE01
  -t TYPE, --type TYPE  Queue Type: classic/quorum
  -d DURABLE, --durable DURABLE
                        Queue durable: true/false

```

