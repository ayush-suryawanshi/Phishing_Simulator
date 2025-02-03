import os
import pandas as pd
import smtplib
from core.models import Employee,Scheme
from dotenv import load_dotenv
from django.shortcuts import render
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from string import Template
#........................................................................................
load_dotenv()
#.........................................................................................

# Function to send email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the MIME message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach the email body
        message.attach(MIMEText(body,'html'))

         # Use SMTP_SSL for encrypted connection
        smtp_server = "smtp.gmail.com"
        smtp_port = 465  # SSL port
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password) # Use the Gmail app password for 2FA authentication . 
            server.send_message(message)
        
        # Close the connection
        server.quit()
    except Exception as e:
        return

#........................................................................................................


def submit_data(requests):
    if requests.method == 'POST':
        scheme_name = requests.POST.get('scheme_name')
        email_file = requests.FILES.get('email_file')
        email_subject = requests.POST.get('email_subject')
        email_body = requests.POST.get('email_body')

        if '.xlsx' in str(email_file) and len(str(email_subject)) > 0 and len(str(email_subject)) > 0:
            new_sceheme = Scheme(scheme_name = scheme_name,
                                 email_file = email_file,
                                 email_subject=email_subject,
                                 email_body=email_body)
            new_sceheme.save()

            df = pd.read_excel(email_file)
            employee_data = df.to_numpy()

            for row in employee_data:
                if Employee.objects.filter(employee_email=row[3]).exists() == False:
                    new_employee = Employee(
                        employee_id = row[0],
                        employee_name = row[1],
                        employee_type = row[2],
                        employee_email = row[3]
                    )

                    new_employee.save()

                custom_filter = str(row[0]).replace('/','_')
                custom_url = f'http://192.168.0.104/confirm_booking/{custom_filter}'

                email_1 = Template(str(email_body))
                final_email_body = email_1.substitute(custom_url=custom_url)

                send_email(sender_email=os.getenv('SENDER_EMAIL'),
                           sender_password=os.getenv('SENDER_PASSWORD'),
                           recipient_email=row[3],
                           subject=email_subject,
                           body=final_email_body)
    return requests

#.............................................................................................

def click_confirmation(requests,employee_id):
    employee_id = str(employee_id).replace('_','/')
    employee_object = Employee.objects.get(employee_id=employee_id)

    employee_object.clicked_link = True

    return
#.........................................................................................

def create_scheme(requests):
    return render(requests,'core/bulk_upload.html')