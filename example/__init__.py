import wrts, json

with open("creds.json") as f:
	creds = json.loads(f.read())

def start():
	session = wrts.login(creds["email"], creds["password"], ".TOKEN")

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
