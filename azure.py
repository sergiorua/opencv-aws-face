import requests

class AzureCognitive:
    url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0'
    key = None

    def __init__(self, key, url=None):
        self.key = key
        if url:
            self.url = url
        CF.BaseUrl.set(self.url)

    def detect(self, image):
        payload = {
            'url': image
        }
        headers = {
            'user-agent': 'serg-app/0.0.1',
            'Ocp-Apim-Subscription-Key': self.key
        }
        ret = requests.post(self.url+'/detect', json=payload, headers=headers)
        return ret.json()
