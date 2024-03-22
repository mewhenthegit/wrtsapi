from .User import User
import requests

class NotifError(Exception):
	pass

class Notif:
	def __init__(self, obj, session):
		self.session = session
		self.id = obj["id"]
		self.created_at = obj["created_at"]
		self.icon = obj["icon"]
		self.image = obj["image"] # ???
		self.is_recent = obj["is_recent"]
		self.landing_url = obj["landing_url"]
		self.message = obj["message"]
		self.read = obj["read"]
		self.retrieved_at = obj["retrieved_at"] # aka read_at i think
		self.creator = User(obj["creator"]["public_profile_name"],session)
	def read(self):
		resp = requests.patch(f"https://api.wrts.nl/api/v3/users/notifications/{self.id}",headers={"x-auth-token": self.session.token}).json()
		if not resp["success"]:
			raise NotifError(resp["error"]+"..... bro how did you mess up reading a notification") # bro how does one even mess that up
		return true
