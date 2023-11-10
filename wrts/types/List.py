from wrts.types.User import User
from wrts.types.Subject import Subject
import requests


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
        self.subjects = (Subject(obj) for obj in obj["subjects"])

