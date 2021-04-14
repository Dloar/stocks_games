import json
import boto3
import logging
import time
import os
import pandas as pd
from datetime import datetime
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket='stocks-list-poi', Key='selected-stocks/whole_selection/stocks_output.json')
    data = pd.read_json(response['Body'].read().decode('utf-8'), lines=True)
    lenght_data = len(data['longName'])
    logging.warning(len(data['longName']))
    body = response['Body'].read()
    last_modified = response["LastModified"]
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = f'SES Update <{json.loads(os.environ["email_list"])["SENDER"]}>'

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = json.loads(os.environ["email_list"])["RECIPIENT"]

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-central-1"

    # The subject line for the email.
    SUBJECT = f'Data update on {datetime.now():%d, %B, %Y %H:%m}'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Data update succesfully done.</h1>
      <p>This email was sent with 
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'> AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an warning if something goes wrong.
    except ClientError as e:
        logging.warning(e.response['warning']['Message'])
    else:
        logging.warning("Email sent! Message ID:"),
        logging.warning(response['MessageId'])

    return str(last_modified)
