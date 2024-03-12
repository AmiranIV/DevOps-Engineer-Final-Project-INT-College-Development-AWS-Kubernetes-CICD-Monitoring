import flask
from flask import request
import os
import signal
import sys
import boto3
from bot import Bot, ImageProcessingBot

app = flask.Flask(__name__)
kms_key_id = 'a691b4da-dd5e-452d-800d-0789cfa27a22'
# Create a KMS client
kms_client = boto3.client('kms', region_name='eu-north-1')
# Retrieve the key
response = kms_client.describe_key(KeyId=kms_key_id)
# The key details can be found in the 'KeyMetadata' field of the response
key_metadata = response['KeyMetadata']
TOKEN = key_metadata['Description']

# # TODO load TELEGRAM_TOKEN value from Secret Manager
TELEGRAM_TOKEN = TOKEN

TELEGRAM_APP_URL = "amiraniv-polybot-dev.devops-int-college.com"

# Global variable to track server readiness
server_ready = False

@app.route('/', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    if not server_ready:
        return 'Server not ready', 503
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


@app.route(f'/results/', methods=['GET'])
def results():
    prediction_id = request.args.get('predictionId')

    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table_name = 'AmiranIV-Dev-Dynamo'  # Replace with your table name
    table = dynamodb.Table(table_name)

    # Define your primary key
    primary_key = {
        'prediction_id': str(prediction_id)
    }

    # Use the get_item method to fetch the item
    response = table.get_item(Key=primary_key)

    # Check if the item was found
    if 'Item' in response:
        item = response['Item']
        print("Item found:")
        print(item['detected_objects'])
        print(item['chat_id'])

        chat_id = item['chat_id']
        text_results = item['detected_objects']

        bot.send_text(chat_id, text_results)
        return 'Ok'
    else:
        print("Item not found")
        return 'Item not found', 404


@app.route(f'/loadTest/', methods=['POST'])
def load_test():
    if not server_ready:
        return 'Server not ready', 503
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


@app.route('/ready', methods=['GET'])
def ready():
    if server_ready:
        return 'Server is ready', 200
    else:
        return 'Server is not ready', 503


# Define a signal handler to catch termination signals
def signal_handler(sig, frame):
    global server_ready
    print('Shutting down gracefully...')
    server_ready = False
    # Perform cleanup tasks here if needed
    sys.exit(0)

# Register the signal handler for SIGTERM signal
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    bot = ImageProcessingBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)
    server_ready = True  # Set server to ready state

    app.run(host='0.0.0.0', port=8443)
