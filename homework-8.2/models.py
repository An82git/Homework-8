from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField

class Client(Document):
    fullname = StringField()
    age = IntField()
    email = StringField()
    phone = StringField()
    method_sending = StringField()
    newsletter_flag = BooleanField(default=False)