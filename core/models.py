from django.db import models
import uuid
#..........................................................

class Scheme(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,primary_key=True)
    scheme_name = models.CharField(editable=False,max_length=100)
    email_file = models.FileField(upload_to='upload/receiver_email_data')
    email_subject = models.CharField(max_length=2000,editable=False)
    email_body = models.CharField(editable=False,max_length=2000)

class Employee(models.Model):
    employee_id = models.CharField(max_length=40,editable=False,primary_key=True,blank=False)
    employee_name = models.CharField(max_length=100,editable=False,default='N/A')
    employee_type = models.CharField(max_length=100,editable=False,default='N/A')
    employee_email = models.CharField(max_length=100,editable=False,default='N/A')
    clicked_link = models.BooleanField(default=False,editable=True)
