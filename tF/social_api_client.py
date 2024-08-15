import requests

API_BASE_URL = "http://localhost:5003"  # Asume que la otra app corre en el puerto 5003

def get_all_users():
    response = requests.get(f"{API_BASE_URL}/api/users")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_user(user_id):
    response = requests.get(f"{API_BASE_URL}/api/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def search_users(query):
    response = requests.get(f"{API_BASE_URL}/api/users/search", params={'q': query})
    if response.status_code == 200:
        return response.json()
    else:
        return None