import wrts, json

f = open("CREDS.txt")
c = json.loads(f.read())
f.close()

def look4sub(subs, target):
	for sub in subs:
		if sub.name == target:
			return sub

def test_subjects():
	s = wrts.Session(c["user"], c["pass"])
	q = s.get_question(250732)
	print(q.user.first_name)
	print("Topic: "+q.topic.title)
	print("Subject: "+q.subject.name)
	sub = look4sub(s.subjects,"Frans")
	topic = sub.topics[0]
	label, count, questions = q.get_related_questions()
	print(f"Similar questions to {label}: {count}")
	sim = next(questions)
	print(f"Example: {sim.title}")
	total, notifs = s.get_notifs(1)
	print(f"There are {total} notifications!")
	notif = next(notifs)
	print(f"{notif.creator.first_name}: {notif.message}")
	#print(s.post_question("Hoe leer je voor frans lol",sub,topic).title)
	assert False
