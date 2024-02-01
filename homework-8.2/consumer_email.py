from connect import connect_rabbit, connect
from models import Client

import json


def sending_massage(email: str) -> None:
    print(email)

def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    for id in message:
        ob = Client.objects(id=id).first()
        
        if not ob.newsletter_flag:
            sending_massage(ob.email)
            ob.update(newsletter_flag = True)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def receiving_message(queue:str):
    with connect_rabbit() as connection:
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue,
                              on_message_callback=callback
                              )
        channel.start_consuming()


if __name__ == "__main__":
    receiving_message("email")
