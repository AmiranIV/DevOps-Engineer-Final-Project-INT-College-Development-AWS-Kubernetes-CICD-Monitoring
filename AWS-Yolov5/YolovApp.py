import time
import boto3
import uuid
import pymongo
import requests
import torch
import json
from PIL import Image
from flask import Flask, request, jsonify
from loguru import logger
import boto3
from bson import json_util
import os

#AWS
images_bucket = "s3amiranivaug"
queue_name = "AmiranIV-AWS-Queue"
#AWS-CLIENTS
sqs_client = boto3.client('sqs', region_name='eu-north-1')
s3_client = boto3.client('s3')
#Model IMPORTING
model = torch.hub.load("ultralytics/yolov5", "yolov5s")
model.eval()

def consume():
    while True:
        response = sqs_client.receive_message(QueueUrl=queue_name, MaxNumberOfMessages=1, WaitTimeSeconds=5)

        if 'Messages' in response:
            message = response['Messages'][0]['Body']
            receipt_handle = response['Messages'][0]['ReceiptHandle']

            # Use the ReceiptHandle as a prediction UUID
            prediction_id = response['Messages'][0]['MessageId']
            # print(message, prediction_id)
            # Extract img_name and chat_id from message
            img_name = f"{message}.jpeg"
            chat_id = message

            if img_name and chat_id:
                # Download the image from S3
                original_img_path = f"/app/{img_name}"
                s3_key = f"{images_bucket}/{img_name}"
                s3_client.download_file(images_bucket, img_name, original_img_path)
                # print(f"img_name: {img_name}, chat_id: {chat_id}, prediction_Id: {prediction_id}")
                time.sleep(4)
                #PREDICTION#
                # Load the image
                img = Image.open(original_img_path)
                # Run inference
                results = model(img)
                predicted_img_path = f'/app/{prediction_id}.jpeg'
                r_img = results.render()  # returns a list with the images as np.array
                img_with_boxes = r_img[0]  # image with boxes as np.array
                img_with_boxes_pil = Image.fromarray(img_with_boxes)
                img_with_boxes_pil.save(predicted_img_path)
                s3_client.upload_file(predicted_img_path, images_bucket, f'{prediction_id}.jpeg')
                time.sleep(3)
                labels = []

                for label in results.pred[0]:
                    class_index = int(label[5])
                    class_name = model.names[class_index]
                    cx, cy, width, height = label[0:4]
                    labels.append({
                        "class": class_name,
                        "cx": cx.item(),
                        "cy": cy.item(),
                        "width": width.item(),
                        "height": height.item()
                    })

                output_json = {
                    "prediction_id": str(prediction_id),
                    "original_img_path": original_img_path,
                    "predicted_img_path": predicted_img_path,
                    "labels": labels,
                }
                # Serialize the output_json using json_util
                output_json_serialized = json.loads(json_util.dumps(output_json))

                # Save the JSON to a file
                output_json_path = f'/app/output_{prediction_id}.json'
                with open(output_json_path, 'w') as json_file:
                    json.dump(output_json, json_file, indent=4)


                # Initialize a dictionary to store the class counts
                class_counts = {}
                # Iterate through the labels and count the occurrences of each class
                for label in output_json['labels']:
                    class_name = label['class']
                    if class_name in class_counts:
                        class_counts[class_name] += 1
                    else:
                        class_counts[class_name] = 1
                message = ""
                for class_name, count in class_counts.items():
                    message += f"{class_name}: {count}\n"
                    Files2DynamoDB = {
                        "prediction_id": str(prediction_id),
                        "chat_id": str(chat_id),
                        "detected_objects": str(message)
                    }
                dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
                dynamoTable = dynamodb.Table('AmiranIV-AWS')
                dynamoTable.put_item(Item=Files2DynamoDB)
                time.sleep(2)

                url = f'http://APPLICATION-LOAD-BALANCER-URL.com'/results/?predictionId={prediction_id}'
                requests.get(url=url)
                time.sleep(7)

            # Delete the message from the queue
            sqs_client.delete_message(QueueUrl=queue_name, ReceiptHandle=receipt_handle)

consume()
