import requests
from core.config import settings

class APIClient:
    def __init__(self, token: str = None):
        self.base_url = settings.API_URL
        self.token = token

    def _headers(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}" 
        return headers

    def get(self, path: str, params: dict = None):
        return requests.get(self.base_url + path, headers=self._headers(), params=params)

    def post(self, path: str, json: dict = None, data: dict = None, files: dict = None):
        return requests.post(self.base_url + path, headers=self._headers(), json=json, data=data, files=files)

    def put(self, path: str, json: dict = None):
        return requests.put(self.base_url + path, headers=self._headers(), json=json)

    def delete(self, path: str):
        return requests.delete(self.base_url + path, headers=self._headers())
