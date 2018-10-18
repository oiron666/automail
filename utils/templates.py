import os
import datetime
import random

def get_template_path(path):
    file_path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.isfile(file_path):
        raise Exception("This is not a valid path %s")
    return file_path

def get_template(path):
    file_path = get_template_path(path)
    return open(file_path).read()

def render_context(template_string, context):
    return template_string.format(**context)

def get_date():
    today = datetime.date.today()
    date_text = '{today.month}/{today.day}/{today.year}'.format(today=today)
    return date_text

def get_random_int():
    total_random = str(random.randint(0,10))
    return total_random
