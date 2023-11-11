from wrts.types.User import User
from wrts.types.Subject import Subject
from datetime import datetime
import requests

class Result:
    def __init__(self, obj):
        self.id = obj["id"]
        self.grade = obj["grade"]
        self.started = datetime.strptime(obj["started_at"], "%Y-%m-%dT%H:%M:%S.000Z")
        self.finished = datetime.strptime(obj["finished_at"], "%Y-%m-%dT%H:%M:%S.000Z")
        self.exercise_type = obj["exercise_type_code"]
        self.errors = obj["wrong_answers_count"]
        self.corrects = obj["correct_answers_count"]
        self.accuracy = obj["correctness_percentage"]
        self.practiced_percentage = obj["practiced_words_percentage"]
        self.practiced = obj["words_practiced"]
        self.listlength = obj["words_in_lists"]
        self.first_attempts = (obj["first_attempts_correctness"]["correct"], obj["first_attempts_correctness"]["incorrect"])


class List:
    def __init__(self, id, session):
        obj = requests.get(f"https://api.wrts.nl/api/v3/public/lists/{id}").json()
        
        self.id = id
        self.session = session

        self.title = obj["title"]
        self.creator = User(obj["creator"]["public_profile_url"], session)
        self.times_practiced = obj["times_practiced"]
        self.shared = obj["shared"]
        self.deleted = obj["deleted"]
        self.rated_words = obj["words_with_performance"] # properly transform this one
        self.book = obj["book"] # same goes for this one
        self.related_topics = obj["related_topics"] # this too
        self.paused_exercise = obj["paused_exercise"] # aswell
        self.status = obj["status"]
        self.upgrade_required = obj['needs_upgrade']
        self.minrole = obj["min_required_role"]
        self.word_count = obj["word_count"]
        self.upgrade_info = obj["upgrade_info"]
        self.related_type = obj["related_topics_type"]
        self.chapter = obj["chapter"] # transform/parse/whatevver
        self.subjects = (Subject(obj) for obj in obj["subjects"])
        self.prioritylang = obj["prioritized_language"]
        self.locales = obj["locales"]

    def get_results(self):
        resp = requests.get(f"https://api.wrts.nl/api/v3/results?list_id={self.id}", headers={"x-auth-token": self.session.token}).json()["results"]
        return (Result(res) for res in resp)