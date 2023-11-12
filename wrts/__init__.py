from .Session import *
import requests, json, os, time

def get_token(email, password) -> dict:
	resp = requests.post("https://api.wrts.nl/api/v3/auth/get_token", json={"email": email, "password": password}).json()
	return resp


def save_token(email, password, path) -> dict:
	with open(path, "w+") as f:
		resp = get_token(email, password)
		f.write(json.dumps(resp))
	return resp

def load_from_file(path) -> dict:
	try:
		with open(path) as f:
			data = json.loads(f.read())
			return data
	except json.decoder.JSONDecodeError:
		return {"success": False}


def login(email, password, path=".WRTS") -> Session:
	try:
		token = load_from_file(path)
		if not token["success"]:
			raise FileNotFoundError("duck!!!")
		if time.time() > token["expires_at"]:
			raise FileNotFoundError("Duck!!!!")

	except FileNotFoundError:
		token = save_token(email, password, path)

	return Session(token)
