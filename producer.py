# amqps://gomriutw:z5EbOXeymZUDKa1MHZSUc_RTUoJljKYF@puffin.rmq2.cloudamqp.com/gomriutw
import pika, json

params      = pika.URLParameters('amqps://gomriutw:z5EbOXeymZUDKa1MHZSUc_RTUoJljKYF@puffin.rmq2.cloudamqp.com/gomriutw')

connection  = pika.BlockingConnection(params)
channel     = connection.channel()

def publish(method, body):
  properties = pika.BasicProperties()
  channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)