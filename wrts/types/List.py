from wrts.types.User import User
from wrts.types.Subject import Subject
from wrts.enums import ANSWER_TYPES, EXERCISE_TYPES
from datetime import datetime
import requests, random

class PracticeSession:
    def __init__(self, obj, session):
        self.session = session

        self.id = obj["id"]
        self.list_id = list(obj["list_languages"].keys())[0]
        self.words = {o["id"]: o["data"] for o in obj["words"]}
        self.special_chars = obj["special_characters"]
        self.extype = obj["exercise_type_code"]
        self.answer_url = obj["answer_url"]
        self.onboarding = obj["show_onboarding"]
        self.all_config = obj["all_configuration"]
        self.legit_config = obj["legit_configuration_values"] # ???
        self.simplified_attemps = obj["simplified_attempts"] #??????/
        self.word_queue = obj["word_queue"]
        self.logic_params = obj["logic_parameters"] # ???????????????????????????
        self.typochecker = obj["allow_typochecker"]
        self.langs = obj["list_languages"][self.list_id]
        self.config = obj["configuration"]

        self.word_queue = []
        self.progress = 0
        self.finished = False
        self.answer_locale = self.config[0]["settings"][0]["value"]
        self.question_locale = ""

        for i, lang in enumerate(self.langs):
            if not lang["locale"] == self.answer_locale:
                self.question_locale = lang["locale"]

        if self.config[0]["settings"][1]["value"]:
            random.shuffle(self.words)

        match self.extype:
            case EXERCISE_TYPES.LEARN:
                self.generate_learn_queue()
            case EXERCISE_TYPES.TEST:
                self.generate_test_queue()

    def push_to_queue(self, display_type: str, word_id: str, roundnr=1):
        if word_id=="": return # dumb hack for generate_learn_queue
        self.word_queue.append({
            "answer_locale": self.answer_locale,
            "correct": None,
            "display_type": display_type,
            "list_id": self.list_id,
            "question_locale": self.question_locale,
            "round_nr": roundnr,
            "word_id": word_id
        })

    def generate_test_queue(self):
        for wordid in self.words:
            self.push_to_queue(ANSWER_TYPES.FULL, wordid)

    def generate_learn_queue(self):
        words_keys = list(self.words.keys())
        words_list = [(words_keys[i], words_keys[i+1]) for i in range(len(words_keys)//2)]
        if not len(words_keys)//2*2 == len(words_keys): words_list.append((words_keys[-1],""))

        for pair in words_list:
            self.push_to_queue(ANSWER_TYPES.LEARN, pair[0])
            self.push_to_queue(ANSWER_TYPES.LEARN, pair[1])

            self.push_to_queue(ANSWER_TYPES.MULTIPLE_CHOICE, pair[0])
            self.push_to_queue(ANSWER_TYPES.MULTIPLE_CHOICE, pair[1])
            
            self.push_to_queue(ANSWER_TYPES.HINTED, pair[0])
            self.push_to_queue(ANSWER_TYPES.HINTED, pair[1])
            
            self.push_to_queue(ANSWER_TYPES.FULL, pair[0])
            self.push_to_queue(ANSWER_TYPES.FULL, pair[1])



    def get_question(self):
        wid = self.word_queue[self.progress]["word_id"]
        
        retval = None
        match self.word_queue[self.progress]["display_type"]:
            case ANSWER_TYPES.LEARN:
                retval = (self.words[wid][self.question_locale], self.words[wid][self.answer_locale])

            case ANSWER_TYPES.MULTIPLE_CHOICE:
                options = [self.words[wid][self.answer_locale]]
                while len(options) < 4:
                    candidate = self.words[random.choice(list(self.words.keys()))][self.answer_locale]
                    if not candidate == self.words[wid][self.answer_locale]:
                        options.append(candidate)
                
                retval = (self.words[wid][self.question_locale], options)
            case ANSWER_TYPES.HINTED:
                retval = (self.words[wid][self.question_locale], self.words[wid][self.answer_locale][0])

            case ANSWER_TYPES.FULL:
                retval = self.words[wid][self.question_locale]

        return retval, self.word_queue[self.progress]["display_type"]

    def answer(self, answer):
        if self.progress == len(self.word_queue)-1:
            self.finished = True

        wid = self.word_queue[self.progress]["word_id"]

        if self.words[wid][self.answer_locale] == answer:
            self.word_queue[self.progress]["correct"] = True
        else:
            self.word_queue[self.progress]["correct"] = False

        if self.extype == EXERCISE_TYPES.LEARN and not self.word_queue[self.progress]["display_type"] == ANSWER_TYPES.LEARN and not self.word_queue[self.progress]["correct"]:
            display_type = self.word_queue[self.progress]["display_type"]
            roundnr = self.word_queue[self.progress]["round_nr"]
            self.push_to_queue(display_type, wid, roundnr)
            self.finished = False

        req = {
            "answer_locale": self.answer_locale,
            "correct_answer": self.words[wid][self.answer_locale],
            "display_type": self.word_queue[self.progress]["display_type"],
            "is_answer_correct": self.word_queue[self.progress]["correct"],
            "is_exercise_finished": self.finished,
            "marked_as_correct_answer": None,
            "provided_answer": answer,
            "question_locale": self.question_locale,
            "round_nr": 1, # handle this correctly next time
            "typochecker_accepted": None,
            "typochecker_shown": False, # These aswell
            "word_id": wid,
            "word_queue": self.word_queue
        }

        if req["display_type"] == ANSWER_TYPES.LEARN:
            del req["correct_answer"]
            req["is_answer_correct"] = True
            self.word_queue[self.progress]["correct"] = True
            req["word_queue"] = self.word_queue

            

        self.progress += 1

        resp = requests.post(self.answer_url, headers={"x-auth-token": self.session.token}, json=req).json()
        return req["is_answer_correct"], resp["success"]
        
        

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
        self.list_length = obj["words_in_lists"]
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

    def practice(self, extype, id=None, selected_words=[]):
        req = {
            "exercise_type_code": extype,
            "id": id,
            "list_ids": [self.id],
            "selected_words": selected_words
        }

        resp = requests.post("https://api.wrts.nl/api/v3/exercises", headers={"x-auth-token": self.session.token}, json=req).json()
        return PracticeSession(resp, self.session)