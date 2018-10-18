import csv
import shutil
from tempfile import NamedTemporaryFile
import datetime
import os
from utils.templates import get_template, render_context, get_date, get_random_int
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

host = "" #mail host
port = 587 #mail port
username = "" #sender email_message
password = ""
from_email = username
to_list = [""]

file_item_path = os.path.join(os.path.dirname(__file__), "data.csv")
class UserManager():

    def get_confirmation(self, user_id = None, email = None, amount = None , sent = None):
        #confirms sending mail by overwriting csv file in the column sent
        filename = file_item_path
        tempfile = NamedTemporaryFile(delete=False)
        with open(filename, 'rb') as csvfile, tempfile:
            reader = csv.DictReader(csvfile)
            fieldnames = ['id', 'name', 'email', 'amount', 'sent', 'date']
            writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                rowstr = str(row['id'])
                userstr = str(user_id)
                if rowstr  == userstr:
                    row['sent'] = "Yes"

                else:
                    pass
                writer.writerow(row)
            shutil.move(tempfile.name, filename)
            return True
        return False

    def send_to_all(self):
        #sends mail to everyone from a file
        i = 1
        length = self.get_length()
        while i < length:
            if self.get_user_data(i) is not None:
                user_details = self.get_user_data(i)
                print(user_details)
                self.message_user(user_id = i)
                self.get_confirmation(user_id = i)
            i += 1
        return "Data sent"

    def get_length(self):
        #checks how many records is in the file
        filename= file_item_path
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            reader_list = list(reader)
        return len(reader_list)

    def render_message(self,user_data):
        #create a message
        path = 'templates/email_message.txt'
        path_html = 'templates/email_message.html'
        template = get_template(path)
        template_html = get_template(path_html)
        date_text = get_date()
        total_random = get_random_int()
        if isinstance(user_data, dict):
            context = user_data
            msg_txt = render_context(template, context)
            msg_html = render_context(template_html, context)
            return msg_txt, msg_html
        return (None, None)

    def message_user(self, user_id = None, email = None):
        #sends an email
        user = self.get_user_data(user_id = user_id, email=email)
        if user:
            user_email = user.get("email")
            to_list.append(user_email)
            msg_txt, msg_html = self.render_message(user)
            print(msg_html)
            try:
                email_conn = smtplib.SMTP(host, port)
                email_conn.ehlo()
                email_conn.starttls()
                email_conn.login(username, password)
                msg = MIMEMultipart("alternative")
                msg["Subject"] = "Hey You"
                msg["From"] = username
                msg["To"] = user_email
                part_1 = MIMEText(msg_txt, 'plain')
                part_2 = MIMEText(msg_html, 'html')
                msg.attach(part_2)
                email_conn.sendmail(msg_html, to_list, msg.as_string())
                email_conn.quit()
            except smptlib.SMTPexception:
                print("error!")
        return "message sent"

    def get_user_data(self, user_id = None, email = None):
        #takes data from csv file
        filename= file_item_path
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            items = []
            unknown_user_id = None
            unknown_email = None

            for row in reader:
                if user_id is not None:
                    if int(row.get('id')) == int(user_id):
                        return row
                    else:
                        unknown_user_id = user_id
                elif email is not None:
                    if row.get('email') == email:
                        return row
                else:
                    unknown_email = email

            if unknown_user_id is not None:
                print("User id {user_id} not found".format(user_id = user_id))
            if unknown_email is not None:
                print("User mail {email} not found".format(email = email))
            return None
        return None
