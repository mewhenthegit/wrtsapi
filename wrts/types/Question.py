from wrts.exceptions import QuestionError
from .Subject import *
from .User import *
import json, requests

class Answer:
	def __init__(self, obj, session):
		self.session = session
		self.body = obj["body"]
		self.can_edit = obj["can_edit"]
		self.can_flag = obj["can_flag"]
		self.correct = obj["correct"]
		self.id = obj["id"]
		self.is_flagged = obj["is_flagged"]
		self.is_own_answer = obj["is_own_answer"]
		self.attachments = obj["qna_attachments"]
		self.upvoted_by_self = obj["is_upvoted"]
		self.user = User(obj["user"]["username"], self.session)
	def vote(self):
		result = requests.post(f"https://api.wrts.nl/api/v3/qna/answers/{self.id}/votes", headers={"x-auth-token": self.session.token}).text
		if self.upvoted_by_self:
			self.votes -= 1
			self.upvoted_by_self = False
		else:
			self.votes += 1
			self.upvoted_by_self = True

class Question:
	def __init__(self, id, session):
		obj = requests.get(f"https://api.wrts.nl/api/v3/public/qna/questions/{id}", headers={"X-auth-token": session.token}).json()
		if obj["qna_question"] == None: raise QuestionError("Question not found")
		obj = obj["qna_question"]
		self.session = session
		self.body = obj["body"]
		self.can_answer = obj["can_answer"]
		self.can_edit = obj["can_edit"]
		self.flag = obj["can_flag"]
		self.contents = obj["contents"]
		self.creation = obj["created_at"]
		self.id = id
		self.is_flagged = obj["is_flagged"]
		self.answers = (Answer(a,self.session) for a in obj["other_qna_answers"])
		self.tutor_answers = (Answer(a,self.session) for a in obj["tutor_qna_answers"])
		self.attachments = obj["qna_attachments"] # do not forget to parse this later
		self.moderated = obj["requires_forced_moderation"]
		self.title = obj["title"]
		#self.subject = Subject(obj["subject"],token)
		self.user = User(obj["user"]["username"],self.session)

		subjects = requests.get("https://api.wrts.nl/api/v3/subjects",headers={"x-auth-token": self.session.token}).json()["subjects"]
		for sub in subjects:
			if sub["id"] == obj["subject"]["id"]:
				self.subject = Subject(sub,session)
				break
		if not obj["topic"] == None:
			for topic in self.subject.topics:
				if topic.id == obj["topic"]["id"]:
					self.topic = topic
					break
	def answer(self, body, attachments=[]):
		resp = requests.post(f"https://api.wrts.nl/api/v3/qna/questions/{self.id}/answers", json={"qna_answer":{"body": body, "qna_attachments_attributes": attachments}}, headers={"X-Auth-Token": self.session.token}).json()
		return Answer(resp["qna_answer"]["id"], self.session)
	def get_related_questions(self):
		resp = requests.get(f"https://api.wrts.nl/api/v3/public/qna/questions/{self.id}/related_questions", headers={"x-auth-token":self.session.token}).json()
		return resp["label"], resp["total_count"], (Question(o["id"],self.session) for o in resp["qna_questions"])

	def report(self, reason):
		resp = requests.post("https://api.wrts.nl/api/v3/qna/flagged_questions", headers={"x-auth-token"}, json={"qna_question_id": self.id, "qna_question_flagging_reason": reason}).json
		return resp

