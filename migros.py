import json
import query as qy
import random
import numpy as np
import pymongo as mg

coll = mg.MongoClient()['migros']['lebensmittel']

def RandNumGen(x, y):
    return random.randint(x, y-1)

def SelectRandomUser(whole):
    rand_id = RandNumGen(0, whole)
    return rand_id

def GenerateQuestions(user):
    pdttypes = list(coll.distinct('lowest_category'))
    perm = iter(np.random.permutation(pdttypes))

    schweizs = []
    bios = []
    umwelt = []
    gesundheit = []

    ## Multiple countries
    while True:
        subtit = next(perm)
        num = coll.find( {
            'lowest_category': subtit,
            'organic': True,
            'info.image.medium': {'$exists':True},
        }).count()
        if len(bios) < 5 and coll.find( {
            'lowest_category': subtit,
            'organic': {'$exists': True},
            'info.image.medium': {'$exists':True},
        }).count() > num and num > 0:
            bios.append(subtit)
            print 'added'
            continue

        num = coll.find( {
            'lowest_category': subtit,
            'country': 'CH',
            'info.image.medium': {'$exists':True},
        }).count()
        if len(schweizs) < 5 and coll.find( {
            'lowest_category': subtit,
            'country': {'$exists': True},
            'info.image.medium': {'$exists':True},
        }).count() > num and num > 0:
            schweizs.append(subtit)
            continue

        num = coll.find( {
            'lowest_category': subtit,
            'environment': {'$gte': 0.5},
            'info.image.medium': {'$exists':True},
        }).count()
        if len(umwelt) < 5 and coll.find( {
            'lowest_category': subtit,
            'environment': {'$exists': True},
            'info.image.medium': {'$exists':True},
        }).count() > num and num > 0:
            umwelt.append(subtit)
            continue

        num = coll.find( {
            'lowest_category': subtit,
            'health': {'$gte': 7},
            'info.image.medium': {'$exists':True},
        }).count()
        if len(gesundheit) < 5 and coll.find( {
            'lowest_category': subtit,
            'health': {'$exists': True},
            'info.image.medium': {'$exists':True},
        }).count() > num and num > 0:
            gesundheit.append(subtit)
            continue

        if len(gesundheit) >= 5 and len(umwelt) >= 5  \
            and len(schweizs) >= 5 and len(bios) >= 5:
            break

    Pdts = []

    for c in bios:
        Pdts.append( (
          coll.find_one( {
            'lowest_category': c,
            'organic': True,
            'info.image.medium': {'$exists':True},
          }),
          coll.find_one( {
            'lowest_category': c,
            'organic': False,
            'info.image.medium': {'$exists':True},
          }),
          ))

    for c in schweizs:
        Pdts.append( (
          coll.find_one( {
            'lowest_category': c,
            'country': 'CH',
            'info.image.medium': {'$exists':True},
          }),
          coll.find_one( {
            'lowest_category': c,
            'country': {'$ne': 'CH'},
            'info.image.medium': {'$exists':True},
          }),
          ))

    for c in umwelt:
        Pdts.append( (
          coll.find_one( {
            'lowest_category': c,
            'environment': {'$gte': 0.5},
            'info.image.medium': {'$exists':True},
          }),
          coll.find_one( {
            'lowest_category': c,
            'environment': {'$lt': 0.5},
            'info.image.medium': {'$exists':True},
          }),
          ))

    for c in gesundheit:
        Pdts.append( (
          coll.find_one( {
            'lowest_category': c,
            'health': {'$gte': 7},
            'info.image.medium': {'$exists':True},
          }),
          coll.find_one( {
            'lowest_category': c,
            'health': {'$lt': 7},
            'info.image.medium': {'$exists':True},
          }),
          ))

        return [({'health':x['health'],
            'organic':x['organic'],
            'country':x['country'],
            'environment':x['environment'],
            'name':x['name'],
            'id':x['id'],
            'image':x['info']['image']['medium'] if 'image' in x['info'] else None
            }, {'health':y['health'],
            'organic':y['organic'],
            'country':y['country'],
            'environment':y['environment'],
            'name':y['name'],
            'id':y['id'],
            'image':y['info']['image']['medium'] if 'image' in y['info'] else None
            }) for (x,y) in Pdts]

def SavePreferences(user, question_list, answers):
	pass

def PersonalityTest(question_list, answers):
	pass

if __name__ == "__main__":
    customer_ids = qy.all_customer_id()
    rand_id = SelectRandomUser(len(customer_ids))
    user_id = customer_ids[rand_id]
    print "user_id:", user_id
    alle_cate = qy.AllLeafCategories()
    #print json.dumps(list(alle_cate), indent=2)

    print json.dumps(qy.CategoriesInfo("1262306"),indent=2)
    """
    trans_history = qy.transaction(user_id)
    #print json.dumps(trans_history, indent=2)
    prod1 = RandNumGen(0, len(trans_history))
    prod1_ean = trans_history[prod1]['migrosEan']
    prod1_infoful = qy.ProductsInfo(prod1_ean, 1)
    print json.dumps(prod1_infoful, indent=2)
    prod1_info = prod1_infoful['catPath']
    print prod1_info
    print prod1_info[len(prod_info)-1]
    """

