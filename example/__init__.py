from pathlib import Path
import wrts, json

DIR = Path(__file__).parents[0]
CREDS = DIR / "creds.json"
TOKEN = DIR / ".TOKEN"


with open(CREDS) as f:
	creds = json.loads(f.read())

def start():
	session = wrts.login(creds["email"], creds["password"], TOKEN)

	print("===== PULLING QUESTIONS =====")
	qcount, questions = session.get_questions()
	if qcount > 0:
		q = next(questions)
		print(q.title, q.body)
		print(type(q.subject.locale))
	else:
		print("No questions detected, should never happen so get inside your bunker")

	print("===== PULLING RELATED QUESTIONS =====")
	label, qcount, questions = q.get_related_questions()
	print(label, qcount)
	if qcount > 0:
		q = next(questions)
		print(q.title, q.subject)
	else:
		print("No related questions")

	print("===== PULLING NOTIFS =====")
	count, notifs = session.get_notifs(1)
	print(f"{count} notifs")
	if count > 0:
		notif = next(notifs)
		print(notif.message)
	else:
		print("No notifications")

	print("===== PULLING LISTS =====")
	user = session.get_self()
	try:
		l = next(user.get_lists())
		print(l.title)
		print(next(l.get_results()))
		learn = l.practice(wrts.enums.EXERCISE_TYPES.LEARN)
		while not learn.finished:
			print(f"Question: {learn.get_question()}")
			answer = input("Answer: ")
			success = learn.answer(answer)
			print(success)
	except StopIteration:
		print("No lists")