class FLAGGING_TYPES:
	INAPPROPRIATE = 1
	CONTAINS_LINK = 2
	WRONG_SUBJECT = 3
	ADVERTISING   = 4
	PERSONAL_INFO = 5

class PERFORMANCE_ORDER:
	WRONG = 0
	MOSTLY_WRONG = 1
	SOMETIMES_WRONG = 2
	MOSTLY_RIGHT = 3
	GOOD = 4
	NOT_PRACTICED = 5

class EXERCISE_TYPES:
	LEARN = 'learn'
	DICTATE = 'dictate'
	TEST = 'full_word'
	HINTS = 'hints'
	MENTAL = 'in_your_mind'
	MULTIPLE_CHOICE = 'multiple_choice'

class BATTLE_EXERCISE_TYPES:
	TEST = 'full_word'
	HINTS = 'hints'
	MULTIPLE_CHOICE = 'multiple_choice'
	SPELLING = 'timed'

class ANSWER_TYPES:
	FULL = 'full_word'
	LEARN = 'learn'
	MULTIPLE_CHOICE = 'multiple_choice'
	HINTED = 'hints'