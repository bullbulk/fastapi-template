# This is a base guide for understanding this project and start to extend its API

# TODO: Replace with interactive version

import requests

# First admin profile from .env
# With this profile you can create other admins
admin_data = {
    "password": "qwerty",
    "username": "admin@oaip.com",  # email in creating == username in getting token
    "fingerprint": "some unique string"
}

# ****************************************** LOGIN GUIDE ******************************************

# Get a pair of access and refresh token for admin profile.
# Refresh expires after 60 days, access - 30 minutes (config.py)
# Access token stores nowhere. Profile ID is included in both tokens and encrypted
# Refresh token stores in database for the opportunity of disabling it in case of unauthorized access
response = requests.post("http://localhost:5555/api/v1/login/", data=admin_data)

# We need to save access token in memory
# This is a key for all our user-specified API requests
tokens = response.json()
# Then use it as header like that
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
# In any time, we can test this token and decide: use this active token or get new one
requests.post(f"http://localhost:5555/api/v1/login/test-token", headers=headers)

# Refreshing tokens: after expiring access token, we need to get new one using refresh token.
# Refresh token is disposable and becomes useless after request
refresh_data = {
    "refresh_token": tokens["refresh_token"],
    "fingerprint": "some_unique_string"
}
# Fingerprint is a unique identifier of device
# The value of this parameter is the responsibility of the client
# Available refresh token and fingerprint give full access to the account
# So fingerprint must be a complex value: browser fingerprint, mobile device id, etc.
response = requests.post("http://localhost:5555/api/v1/login/update-token", data=refresh_data)
# We must store this token in database
refresh_token = response.json()['refresh_token']
# If refresh token is expired, we need to log in with username and password


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
