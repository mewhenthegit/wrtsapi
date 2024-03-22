from .Session import *
from .exceptions import *
import requests, json, os, time

def get_token(email, password):
	resp = requests.post("https://api.wrts.nl/api/v3/auth/get_token", json={"email": email, "password": password}).json()
	return resp


def save_token(email, password, path):
	with open(path, "w+") as f:
		resp = get_token(email, password)
		f.write(json.dumps(resp))
	return resp

def load_from_file(path):
	try:
		with open(path) as f:
			data = json.loads(f.read())
			return data
	except json.decoder.JSONDecodeError:
		return {"success": False}


def login(email, password, path=".WRTS"):
	try:
		token = load_from_file(path)
		if time.time() > token["expires_at"]:
			raise FileNotFoundError("Sussy")

	except FileNotFoundError:
		token = save_token(email, password, path)

	if not token["success"]:
		raise LoginFailure(token["info"])
	return Session(token)
