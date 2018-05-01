import boto3
import requests
import os

class AWSRecoknition:
    region = 'eu-west-1'
    key_id = None
    access_key = None
    bucket = None

    def __init__(self, key_id=None, access_key=None, bucket=None, region='eu-west-1'):
        self.region = region
        self.key_id = key_id
        self.access_key = access_key
        self.bucket = bucket

    def detect(self, image, attributes=['ALL']):
        rekognition = boto3.client("rekognition", self.region)

        if 'http' in image:
            r = requests.get(image, stream=True)
            img_data = {'Bytes': r.raw.read()}
        elif os.path.exists(image):
            with open(image, 'rb') as i:
                img_data = {'Bytes': i.read()}
        elif bucket is not None:
            img_data={
			    "S3Object": {
				    "Bucket": bucket,
				    "Name": key,
			    }
        else:
            return None

        response = rekognition.detect_faces(
            Image=img_data,
	        Attributes=attributes,
	    )
        return response['FaceDetails']
