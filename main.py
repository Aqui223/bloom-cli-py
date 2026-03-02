import requests
import json
import re
import os

api_url = "https://api.bloomapp.pw"
email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"

if os.path.isfile("authentication.json"):
    with open("authentication.json", "r") as file:
	    authentication = json.load(file)
    logged_in = "bloom-auth-response" in authentication
else:
    logged_in = False

def g(route, data=None, token=None):
    headers = None
    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}
	return requests.get(api_url+route, data, headers=headers)

def p(route, data=None, token=None):
    headers = None
    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}
	return requests.post(api_url+route, data, headers=headers)

if logged_in:
    print("You're not logged in.")

    while True:
        email = input("Your email: ")
        if re.fullmatch(email_regex, email):
            break
    exists = g(f"/user/exists?email={email}").json()["exists"]
    if exists:
        resp = p("/auth/request-code", {"email": email})
        
        print("/request-code", resp.text)
    else:
        resp = p(f"/auth/register?email={email}")
        print(resp.text, "\n", resp.status_code)

    while True:
        code = input("Code in your email: ")
        if code.isdecimal():
            break
    resp = p(f"/auth/verify-code", {"email": email, "code": code})
    print(resp.status_code)
    authentication['bloom-auth-response'] = resp.json()
    TOKEN = authentication['bloom-auth-response']['token']
    authentication['email'] = email

    with open("authentication.json", "w") as file:
        json.dump(authentication, file)

print("The chat itself isn't implemented yet")
