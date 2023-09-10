from wrts.types.User import User
from wrts.types.Subject import Subject
import requests


class List:
	def __init__(self, id, session):
		self.session = session
		self.id = id["id"]

		resp = requests.get(f"https://api.wrts.nl/api/v3/public/lists/{self.id}", headers={"x-auth-token": self.session.token}).json()
		#print(resp)
		self.title = resp["title"]
		self.description = resp["description"]
		self.creator = User(resp["creator"]["public_profile_name"], session)
		self.times_practiced = resp["times_practiced"]
		self.shared = True
		self.deleted = False
		self.performance_order = resp["performance_section_order"] #???
		self.book = resp["book"] # parse this later
		self.exercise_types = resp["exercise_types"] # parse this later
		self.live_exercise_types = resp["live_battle_exercise_types"] # WHAR?? (parse later)
		self.related_topics = resp["related_topics"] # parse later
		self.paused_exercise = resp["paused_exercise"] # paaaarse
		self.status = resp["status"]
		self.paywall = resp["needs_upgrade"]
		self.minroll = resp["min_required_role"]
		self.wordcount = resp["word_count"] # ??
		self.upgrade_info = resp["upgrade_info"] # maybe parse?
		self.related_topics_type = resp["related_topics_type"]
		self.subjects = (Subject(o,session) for o in resp["subjects"])
		#self.subject = Subject(resp["subject"],session)
		self.is_own = resp["is_own_list"] # why can't they just infer this from the creator
		self.is_from_publisher = resp["is_from_publisher"] # for book prob
		self.prioritylang = resp["prioritized_language"] #parse
		self.locales = resp["locales"] # .... parse (also make locales their own file)
		if self.book: self.chapter = resp["chapter"] # parse

