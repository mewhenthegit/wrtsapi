from wrts.Session import Session
import json

f = open("CREDS.txt")
c = json.loads(f.read())
f.close()

def test():
	session = Session(c["user"], c["pass"])
	questions = session.get_questions()
	q = next(questions)
	print(q.title)
	question = session.get_question(243445)
	question.answer("bedankt allemaal!")
	print("answered")
	assert False
