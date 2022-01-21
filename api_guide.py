# This is a base guide for understanding this project and start to extend its API

# TODO: Replace with interactive version

import requests

# First admin profile from .env
# With this profile you can create other admins
admin_data = {
    "password": "qwerty",
    "username": "admin@oaip.com",  # email in creating == username in getting token
}

# ****************************************** LOGIN GUIDE ******************************************

# Get an access token for admin profile, which will expire in 8 days (config.py)
# This token stores nowhere. Profile ID is included in token and encrypted
response = requests.post("http://localhost:5555/api/v1/login/access-token", data=admin_data)

# We need to save this token in memory, database, etc.
# This is a key for all our user-specified API requests
access_token = response.json()["access_token"]
# Then use it as header like that
headers = {"Authorization": f"Bearer {access_token}"}
# In any time, we can test this token and decide what we need: use this validated token or login again
# TODO: Add refresh token support
requests.post(f"http://localhost:5555/api/v1/login/test-token", headers=headers)

# *************************************** CRUD API GUIDE ***************************************

# CRUD - Create Read Update Delete

data_to_create_user = {
    "password": "string",
    "email": "user@example.com",
    "full_name": "string",
    "is_superuser": True  # Not available for open creation
}

# Get all users (you need token of one of the superusers profiles)
requests.get("http://localhost:5555/api/v1/users/", headers=headers)
# Create default user (only available for superuser). Superusers can create other superusers
requests.post("http://localhost:5555/api/v1/users/", json=data_to_create_user, headers=headers)
# Open creation of default user (without need of logging in). It can be disabled in .env
requests.post("http://localhost:5555/api/v1/users/open", json=data_to_create_user)
# Get active profile (which ID is encrypted in used token)
requests.get("http://localhost:5555/api/v1/users/me", headers=headers)
# Read by ID. Superuser can access all profiles, default user only its own
requests.get("http://localhost:5555/api/v1/users/2", headers=headers)

# Get all items of this profile
requests.get("http://localhost:5555/api/v1/items/", headers=headers)
# Create new item for this profile
requests.post("http://localhost:5555/api/v1/items/",
              json={"title": "string", "description": "string"}, headers=headers)
# Read by ID. Default user can access only its own items
requests.get("http://localhost:5555/api/v1/items/2", headers=headers)
# Delete by ID. Default user can delete only ots own items
requests.delete("http://localhost:5555/api/v1/items/2", headers=headers)
