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
	q = next(questions)
	print(q.title, q.body)

	print("===== PULLING RELATED QUESTIONS =====")
	label, qcount, questions = q.get_related_questions()
	print(label, qcount)
	q = next(questions)
	print(q.title, q.subject)

	print("===== PULLING NOTIFS =====")
	count, notifs = session.get_notifs(1)
	print(f"{count} notifs")
	notif = next(notifs)
	print(notif.message)

	print("===== PULLING LISTS =====")
	user = session.get_self()
	print(next(user.get_lists()))
