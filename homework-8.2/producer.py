from connect import connect_rabbit, connect
from models import Client

from faker import Faker
import json


queue = ["SMS", "email"]


def name_generation(num: int) -> list:
    names = []

    for _ in range(num):
        names.append(Faker().name())
    
    return names

def age_generation(num: int) -> list:
    age = []

    for _ in range(num):
        age.append(Faker().random_int(min=18, max=60))
    
    return age

def email_generation(num: int) -> list:
    emails = []

    for _ in range(num):
        emails.append(Faker().email())

    return emails

def phone_generation(num: int) -> list:
    phones = []

    for _ in range(num):
        phones.append(Faker('uk_UA').phone_number())

    return phones

def method_sending_generation(num: int) -> list:
    method_sending_list = []
    method_sending = ["SMS", "email"]

    for _ in range(num):
        method_sending_list.append(Faker().random_element(method_sending))

    return method_sending_list

def contact_generation(num: int) -> None:
    names = name_generation(num)
    age = age_generation(num)
    emails = email_generation(num)
    phones = phone_generation(num)
    method_sending = method_sending_generation(num)

    for index in range(num):
        Client(fullname=names[index],
               age=age[index],
               email=emails[index],
               phone=phones[index],
               method_sending=method_sending[index]
               ).save()

def sending_queue(queue:str) -> None:
    client_id_list = [str(ob.id) for ob in Client.objects().all() if ob.method_sending == queue]

    with connect_rabbit() as connection:
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(client_id_list).encode()
            )

if __name__ == "__main__":
    contact_generation(5)
    [sending_queue(q) for q in queue]
