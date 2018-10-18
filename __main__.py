import argparse

from data_manager import UserManager
from utils.templates import get_template, render_context, get_date, get_random_int

parser = argparse.ArgumentParser(prog = "hungry")
parser.add_argument("type", type=str, choices=['view', 'message', 'sendtoall', 'count'])
parser.add_argument('-id','--user_id', type = int)
parser.add_argument('-e','--email', type = str)

args = parser.parse_args()

if args.type == 'sendtoall':
    print(UserManager().send_to_all())
elif args.type == 'count':
    print(UserManager().get_length())
if args.type == 'view':
    print(UserManager().get_user_data(user_id=args.user_id, email=args.email))
elif args.type == 'message':
    print(UserManager().message_user(user_id=args.user_id, email=args.email))
