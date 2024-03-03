import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
import boto3

class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60,
                                             certificate=open(f'/app/<NAME OF PUBLIC CERT.pem FILE>, 'r'))

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class ImageProcessingBot(Bot):
    def __init__(self, token, telegram_chat_url):
        super().__init__(token, telegram_chat_url)
        self.processing_completed = True

    def handle_message(self, msg):
        if not self.processing_completed:
            logger.info("Previous message processing is not completed. Ignoring current message.")
            return

        if "photo" in msg:
            # If the message contains a photo, check if it also has a caption
            if "caption" in msg:
                caption = msg["caption"]
                if "concat" in caption.lower():
                    self.process_image(msg)
                if "contour" in caption.lower():
                    self.process_image_contur(msg)
                if "rotate" in caption.lower():
                    self.process_image_rotate(msg)
                if "predict" in caption.lower():
                    self.upload_2_S3(msg)

            else:
                logger.info("Received photo without a caption.")
        elif "text" in msg:
            super().handle_message(msg)  # Call the parent class method to handle text messages
    def process_image(self, msg):
        self.processing_completed = False

        # Download the two photos sent by the user
        image_path = self.download_user_photo(msg)
        another_image_path = self.download_user_photo(msg)

        # Create two different Img objects from the downloaded images
        image = Img(image_path)
        another_image = Img(another_image_path)

        # Process the image using your custom methods (e.g., apply filter)
        image.concat(another_image)  # Concatenate the two images

        # Save the processed image to the specified folder
        processed_image_path = image.save_img()

        if processed_image_path is not None:
            # Send the processed image back to the user
            self.send_photo(msg['chat']['id'], processed_image_path)

        self.processing_completed = True
    def process_image_contur(self, msg):
        self.processing_completed = False

        # Download the two photos sent by the user
        image_path = self.download_user_photo(msg)

        # Create two different Img objects from the downloaded images
        image = Img(image_path)

        # Process the image using your custom methods (e.g., apply filter)
        image.contour()  # contur the image

        # Save the processed image to the specified folder
        processed_image_path = image.save_img()

        if processed_image_path is not None:
            # Send the processed image back to the user
            self.send_photo(msg['chat']['id'], processed_image_path)

        self.processing_completed = True

    def process_image_rotate(self, msg):
        self.processing_completed = False

        # Download the two photos sent by the user
        image_path = self.download_user_photo(msg)

        # Create two different Img objects from the downloaded images
        image = Img(image_path)

        # Process the image using your custom methods (e.g., apply filter)
        image.rotate()  # rotate the image

        # Save the processed image to the specified folder
        processed_image_path = image.save_img()

        if processed_image_path is not None:
            # Send the processed image back to the user
            self.send_photo(msg['chat']['id'], processed_image_path)

        self.processing_completed = True


    def upload_2_S3(self, msg):
        self.processing_completed = False
        image_path = self.download_user_photo(msg)
        # Upload the image to S3
        s3_client = boto3.client('s3')
        images_bucket = 's3amiranivaug'
        s3_key = f'{msg["chat"]["id"]}.jpeg'
        s3_client.upload_file(image_path, images_bucket, s3_key)

        time.sleep(3)

        # Create an SQS client
        sqs = boto3.client('sqs',region_name='eu-north-1')
        # Your SQS queue URL (replace with your actual SQS queue URL)
        queue_url =  <'YOUR-AWS-SQS-URL'
>
        # Create a message with a custom message ID
        message_body = str(msg["chat"]["id"])
        message_id = s3_key
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes={
                'CustomMessageID': {
                    'DataType': 'String',
                    'StringValue': message_id
                }
            }
        )

        # Check for a successful response (optional)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f"Message with ID {message_id} sent successfully.")
        time.sleep(3)
        self.send_text(msg['chat']['id'], f'Please wait your image is being processed...')
        self.processing_completed = True
