class FLAGGING_TYPES:
	INAPPROPRIATE = 1
	CONTAINS_LINK = 2
	WRONG_SUBJECT = 3
	ADVERTISING   = 4
	PERSONAL_INFO = 5

class PERFORMANCE_ORDER:
	WRONG = 0
	MOSTLYWRONG = 1
	SOMETIMESWRONG = 2
	MOSTLYRIGHT = 3
	GOOD = 4
	NOTPRACTICED = 5

class EXERCISE_TYPES:
	LEARN = 'learn'
	DICTATE = 'dictate'
	TEST = 'full_word'
	HINTS = 'hints'
	MENTAL = 'in_your_mind'
	MULTIPLECHOICE = 'multiple_choice'

class BATTLE_EXERCISE_TYPES:
	TEST = 'full_word'
	HINTS = 'hints'
	MULTIPLECHOICE = 'multiple_choice'
	SPELLING = 'timed'

def enumify(enum, val):
	for attr in [attr for attr in getattr(enum) if not attr.startswith("__")]:
		if object.__getattribute__(enum, attr) == val:
			return attr