from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField, TextField, TimeField

# Create your models here.
#books表
class Books(models.Model):
    book_name = CharField(max_length=50)
    book_type = CharField(max_length=50)
    book_introduction = TextField()
    issue_year = IntegerField()
    book_file_name = CharField(max_length=100)
    add_book_time = CharField(max_length=100)

