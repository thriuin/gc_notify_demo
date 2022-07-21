import argparse
import base64
import configparser
import json
from notifications_python_client import prepare_upload
from notifications_python_client.notifications import NotificationsAPIClient


# Collect some options from the command line

parser = argparse.ArgumentParser()
parser.add_argument('--apikey', type=str, help='GC Notify API key', default='')
parser.add_argument('--template_id', type=str, help='Template ID', default='') 
parser.add_argument('--email_to', type=str, help='Email address to send test email to', required=True)
parser.add_argument('--name', type=str, help='Email recipient\'s name', default='Bob')
parser.add_argument('--file', type=str, help='File to attach to email', required=True)
args = parser.parse_args()

config = configparser.ConfigParser()
config.sections()
config.read("./gcnotify.ini")

api_key = args.apikey if args.apikey else config['DEFAULT']['default_apikey']
template_id = args.template_id if args.template_id else config['DEFAULT']['demo_template']

# Call out to GC Notify to send the email

notifications_client = NotificationsAPIClient(api_key)

with open(args.file, 'rb') as f:
    contents = f.read()
    response = notifications_client.send_email_notification(
        email_address=args.email_to,
        template_id=template_id,
        personalisation={
            'name': args.name, 
            'file_link': {
                'file': base64.b64encode(contents).decode('ascii'),
                'filename': args.file,
                'sending_method': 'attach'
                }
            }
        )

    print("\nResponse from GC Notify:\n")
    print(json.dumps(response, indent=2))


