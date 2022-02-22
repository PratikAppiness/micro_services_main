# amqps://gomriutw:z5EbOXeymZUDKa1MHZSUc_RTUoJljKYF@puffin.rmq2.cloudamqp.com/gomriutw
import pika, json
from main import Product, db

params      = pika.URLParameters('amqps://gomriutw:z5EbOXeymZUDKa1MHZSUc_RTUoJljKYF@puffin.rmq2.cloudamqp.com/gomriutw')

connection  = pika.BlockingConnection(params)
channel     = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
  print('Received in main')
  data = json.loads(body.decode('utf-8'))
  print(data,properties.content_type)

  if properties.content_type == 'Product Created':
    product = Product(id=data['id'], title=data['title'], image=data['image'])
    db.session.add(product)
    db.session.commit()
    print('Product Created')
  
  elif properties.content_type == 'Product Updated':
    product = Product.query.get(data['id'])
    product.title = data['title']
    product.image = data['image']
    db.session.commit()
    print('Product Updated')

  elif properties.content_type == 'Product Deleted':
    product = Product.query.get(data)
    db.session.delete(product)
    db.session.commit()
    print('Product Deleted')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Start Consuming MAIN')

channel.start_consuming()
channel.close()