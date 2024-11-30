import httpx

class APIClient:
    BASE_URL = "https://example.com/api"

    def __init__(self, token=None):
        self.token = token

    def authenticate(self, email, password):
        response = httpx.post(f"{self.BASE_URL}/auth/login", json={"email": email, "password": password})
        response.raise_for_status()
        return response.json()["token"]
    
    def get_vks(self):
        response = httpx.get(f"{self.BASE_URL}/vks", headers={"Authorization": f"Bearer {self.token}"})
        response.raise_for_status()
        return response.json()

    def create_vks(self, title, date, time, participants):
        payload = {
            "title": title,
            "date": date,
            "time": time,
            "participants": participants,
        }
        response = httpx.post(f"{self.BASE_URL}/vks", json=payload, headers={"Authorization": f"Bearer {self.token}"})
        response.raise_for_status()
        return response.json()

    def delete_vks(self, meeting_id):
        response = httpx.delete(f"{self.BASE_URL}/vks/{meeting_id}", headers={"Authorization": f"Bearer {self.token}"})
        response.raise_for_status()
        return response.json()
    
    def get_vks_by_date(self, date):
        response = httpx.get(f"{self.BASE_URL}/vks/date/{date}", headers={"Authorization": f"Bearer {self.token}"})
        response.raise_for_status()
        return response.json()

    def search_vks(self, query):
        response = httpx.get(
            f"{self.BASE_URL}/vks/search", 
            headers={"Authorization": f"Bearer {self.token}"},
            params={"query": query}
        )
        response.raise_for_status()
        return response.json()

    def search_vks(self, query):
        response = httpx.get(
            f"{self.BASE_URL}/vks/search", 
            headers={"Authorization": f"Bearer {self.token}"},
            params={"query": query}
        )
        response.raise_for_status()
        return response.json()
    
    def process_custom_input(self, user_input):
        response = httpx.post(
            f"{self.BASE_URL}/process_input",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"input": user_input}
        )
        response.raise_for_status()
        return response.json()