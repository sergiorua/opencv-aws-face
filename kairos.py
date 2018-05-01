# curl -d '{"image": "YOUR_IMAGE_URL"}' -H "app_id: YOUR_APP_ID" -H "app_key: YOUR_APP_KEY" 
#   -H "Content-Type: application/json" http://api.kairos.com/detect  

import requests

class Kairos:
    app_id = None
    app_key = None
    url = 'http://api.kairos.com/detect'

    def __init__(self, app_id, app_key, url=None):
        self.app_id = app_id
        self.app_key = app_key
        if url:
            self.url = url

    def detect(self, image):
        payload = {
            'image': image
        }
        headers = {
            'user-agent': 'serg-app/0.0.1',
            'app_id': self.app_id,
            'app_key': self.app_key
        }
        ret = requests.post(self.url, json=payload, headers=headers)
        return ret.json()