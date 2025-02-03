from django.urls import path
from core.views import *

urlpatterns = [
    path('send_email',send_email,name='send_email'),
    path('submit_data',submit_data,name='submit_data'),
    path('confirm_booking/<str:employee_id>',click_confirmation,name='click_confirmation'),
    path('create_scheme',create_scheme,name='create_scheme')
]


/home/jahnwi.tiwary/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock Phishing_Simulator.wsgi:application