from wrts import Session
import json

f = open("CREDS.txt")
creds = json.loads(f.read())
f.close()

def test_attachment():
	session = Session(creds["user"], creds["pass"])
	print(session.upload("../../Desktop/wallpaper.png"))
	assert False

