import boto3
from botocore.exceptions import ClientError
from message.messenger import Messenger

class AWSSESMessenger(Messenger):
    
    def __init__(self, region, access_key_id, secret_access_key):
        self.client = boto3.client('ses', region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    def send(self, sender, recipient, subject, message_text, message_html):
        charset = 'UTF-8'
        try:
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': charset,
                            'Data': message_html,
                        },
                        'Text': {
                            'Charset': charset,
                            'Data': message_text,
                        },
                    },
                    'Subject': {
                        'Charset': charset,
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])


## The email body for recipients with non-HTML email clients.
#  BODY_TEXT = (f"New Submission:\n- {name}\n- {email}")
## The HTML body of the email.
#  BODY_HTML = """<html>
#  <head></head>
#  <body>
#    <p>New Submission:
#    <ul>
#      <li>#NAME#</li>
#      <li>#EMAIL#</li>
#    </ul>
#    </p>
#  </body>
#  </html>
#              """
#  BODY_HTML = BODY_HTML.replace('#NAME#', name).replace('#EMAIL#', email)
