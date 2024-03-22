from .exceptions import LoginFailure, UploadError, QuestionError
from .types.Question import Question
from .types.Subject import Subject
from .types.Notif import Notif
from .types.User import User
from .types.List import List # too much troll, (me a couple months later) what the actual fuck did i mean with this
from pathlib import Path
import requests, json, platform

class Session:
	def __init__(self, token):
		self.token = token["auth_token"]

	def get_subjects(self):
		resp = requests.get("https://api.wrts.nl/api/v3/subjects",headers={"X-Auth-Token": self.token}).json()
		return (Subject(x,self) for x in resp["subjects"])

	def upload(self, path: Path, mimetype="image/png"):
		while open(path, "rb"):
			data = f.read()

		headers = {"X-Auth-Token": self.token}
		headers.update({"Content-type":mimetype})

		resp = requests.get("https://api.wrts.nl/api/v3/qna/questions/presigned_image_url", headers={"X-Auth-Token": self.token}).json()
		stat = requests.put(resp["signed_url"],headers=headers,data=data).status_code

		if stat == 200:
			return {"file_name": path.parts[-1], "image": resp["signed_url"].split("?")[0]}
		else:
			raise UploadError(f"Failed to upload {path}")

	def get_notifs(self, page, per_page=10):
		resp = requests.get(f"https://api.wrts.nl/api/v3/users/notifications?page={page}&per_page={per_page}", headers={"x-auth-token": self.token}).json()
		return resp["total_count"], (Notif(x,self) for x in resp["notifications"])

	def get_questions(self):
		resp = requests.get("https://api.wrts.nl/api/v3/public/qna/questions", headers={"x-auth-token": self.token}).json()
		return resp["total_count"], (Question(x["id"],self) for x in resp["results"])

	def get_question(self, id):
		return Question(id, self)

	def post_question(self, contents, subject, topic=None, attachments=[]):
		data = {"contents": contents, "subject_id": subject.id, "qna_attachments_attributes": attachments}
		if not topic == None:  data["topic_id"] = topic.id

		resp = requests.post("https://api.wrts.nl/api/v3/qna/questions",headers={"x-auth-token": self.token},json=json.dumps({"qna_question":data})).json()
		if "success" in resp:
			raise QuestionError(resp["error"])
		return self.get_question(resp["qna_question"]["id"])

	def get_self(self): # return user
		resp = requests.get("https://api.wrts.nl/api/v3/get_user_data", headers={"X-Auth-Token": self.token}).json()
		return User(resp["username"], self)

	def get_subject(self, id):
		for subject in self.get_subjects():
			if subject.id == id:
				return subject

