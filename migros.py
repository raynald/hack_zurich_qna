import query as qy
import random

def RandNumGen(x, y)
    return random.randint

def SelectRandomUser(whole):
    RandNumGen(0, whole)
    rand_id = random.randint(0, len(whole)-1)
    return rand_id

def GenerateQuestions(user):
	return range(1,16)


def SavePreferences(user, question_list, answers):
	pass

def PersonalityTest(question_list, answers):
	pass

if __name__ == "__main__":
    customer_ids = qy.all_customer_id()
    rand_id = SelectRandomUser(len(customer_ids))
    user_id = customer_ids[rand_id]
    print "user_id:", user_id
    trans_history = transaction(user_id)


