import requests
from config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = None

    def login(self, email, password):
        url = f"{self.base_url}/auth/login"
        response = requests.post(url, json={"email": email, "password": password})
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            return True
        return False

    def get_headers(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    def get_vcs(self, filters=None):
        url = f"{self.base_url}/vcs"
        response = requests.get(url, headers=self.get_headers(), params=filters)
        return response.json()

    def create_vcs(self, data):
        url = f"{self.base_url}/vcs/create"
        response = requests.post(url, headers=self.get_headers(), json=data)
        return response.json()