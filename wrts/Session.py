from .types.Question import Question
import requests, json

class LoginFailure(Exception):
	pass

class Session:
	loggedin = False
	renew = 0
	expiration = 0
	token = ""
	def __init__(self, user, passwd):
		self._login(user, passwd)
	def _login(self, user, passwd):
		resp = requests.post("https://api.wrts.nl/api/v3/auth/get_token", json={"email": user, "password": passwd}).json()
		#print(resp)
		if not resp["success"]:
			raise LoginFailure(resp["info"])
		self.loggedin = True
		self.renew = resp["renew_from"]
		self.expiration = resp["expires_at"]
		self.token = resp["auth_token"]
	def get_questions(self):
		resp = requests.get("https://api.wrts.nl/api/v3/public/qna/questions").json()
		def gen(questions, token):
			for q in questions:
				yield Question(q["id"],self.token)
		return gen(resp["results"], self.token)
	def get_question(self, id):
		return Question(id, self.token)
	def post_question(self, contents, subject, attachments=[]):
		data = {"contents": contents, "subject_id": subject, "qna_attachments_attributes": attachments}
		resp = requests.post("https://api.wrts.nl/api/v3/public/qna/questions",json=json.dumps({"qna_question":data})).json()
		return get_question(resp["id"])
