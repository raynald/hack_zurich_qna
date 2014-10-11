import json
import query as qy
import random

def RandNumGen(x, y):
    return random.randint(x, y-1)

def SelectRandomUser(whole):
    rand_id = RandNumGen(0, whole)
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
    trans_history = qy.transaction(user_id)
    #print json.dumps(trans_history, indent=2)
    prod1 = RandNumGen(0, len(trans_history))
    prod1_ean = trans_history[prod1]['migrosEan']
    prod1_infoful = qy.ProductsInfo(prod1_ean, 1)
    print json.dumps(prod1_infoful, indent=2)
    prod1_info = prod1_infoful['catPath']
    print prod1_info
    print prod1_info[len(prod_info)-1]

