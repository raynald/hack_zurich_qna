#!/usr/bin/env python
# coding=utf-8
import migros
import flask
from flask import Flask
from flask import render_template, session, request

app = Flask(__name__)
app.debug = True
app.secret_key='this key is very secret indeed'

@app.route('/')
@app.route('/quiz')
def quiz():
    # Render the quiz start page
    return render_template('quiz.html')

@app.route('/question/<step>')
def question(step):
    """
    Ask the user the question for this step
    """

    if 'begin' in request.args and int(request.args['begin']):
        session.clear()

    step = int(step)
    print 'Step is %d' % step

    user = None

    if 'question_list' not in flask.session or \
            'answers' not in flask.session:
        session['question_list'] = migros.GenerateQuestions(user) ## initialize this to a list of categories
        session['answers'] = [ None ] * len(session['question_list'])
    else:
        print 'Resued question list %s' % str(flask.session['question_list'])

    if 'question_num' in request.args:
        qn_num = int(request.args['question_num'])
        if qn_num >= 1 and qn_num <= len(session['question_list']):
            if request.args['clicked'] == 'left':
                session['answers'][qn_num - 1] = 0
            elif request.args['clicked'] == 'right':
                session['answers'][qn_num - 1] = 1
            else:
                session['answers'][qn_num - 1] = -1

    total_questions = len(flask.session['question_list'])
    country_flag_map = {
            'ES': '/static/images/spain.png',
            'CH': '/static/images/switzerland.svg',
            'DE': '/static/images/germany.gif',
            'AT': '/static/images/austria.gif',
            'IT': '/static/images/italy.gif',
            'FR': '/static/images/france.gif',
    }

    if step >= total_questions:
        return results()

    args = {
            'image_left_source': session['question_list'][step][0]['image'],
            #'http://migros-cache.fsi-viewer.com/fsicache/server?type=image&source=images%2Fmigros_api%2Fstaging%2Fproduct_204015800000.jpg',
            'image_right_source': session['question_list'][step][1]['image'],
            #'http://migros-cache.fsi-viewer.com/fsicache/server?type=image&source=images%2Fmigros_api%2Fstaging%2Fproduct_204015800000.jpg',
            'lefthealth': session['question_list'][step][0]['health'],
            'righthealth': session['question_list'][step][1]['health'],
            'leftcountry': country_flag_map[session['question_list'][step][0]['country']],
            'rightcountry': country_flag_map[session['question_list'][step][1]['country']],
            'leftorganic': session['question_list'][step][0]['organic'],
            'rightorganic': session['question_list'][step][1]['organic'],
            'leftenvironment': session['question_list'][step][0]['environment'],
            'rightenvironment': session['question_list'][step][1]['environment'],
            'question_num': step,
            'total_questions': 15,
            'form_action': '/question/%d' % (int(step)+1),
            'leftname': session['question_list'][step][0]['name'],
            'rightname': session['question_list'][step][1]['name'],
            };

    # Render the quiz start page
    return render_template('question.html', step=step, **args)

@app.route('/results')
def results():
    """
    Give the user the results of the quiz
    """

    user = None
    migros.SavePreferences( user, session['question_list'], session['answers'] )
    x = migros.PersonalityTest( session['question_list'], session['answers'] )

    if 'debugresult' in request.args.keys():
      x = [ True if c == '0' else False \
            for c in request.args['debugresult']]

    args = {
        'enumerate': enumerate,
        'personality': [

            {
              'adjective': 'A Conscientious Eater',
              'description': """
              You watch what you eat. You need to know what\'s in your food.
              The calories in your food are important to you, as are the vitamins and
              minerals
              """,
              'image': '/static/images/fitman.gif',
            } if x[0] else \
            {
              'adjective': 'You are a Food Lover',
              'description': """
              What is the point of eating food that tastes bad?
              You don't mind sacrificing a couple of years of your life in exchange for
              great tasting daily average food.
              """,
              'image':  '/static/images/foodlover.jpg',
            },

            {
              'adjective': 'No Chemicals Please!',
              'description': """
              You love your stuff <i>au naturel</i>. No artificial colours, flavours, preservatives,
              pesticides, herbicides, fertilizers absolutely in anything that you take into your body.
              """,
              'image': '/static/images/forest.jpg',
            } if x[2] else \
            {
              'adjective': 'Chemicals are an Acceptable Tradeoff',
              'description': """
              You are ambivalent toward organic food.
              You know that Nature is there primarily to defend herself and not to feed you.
              And you acknowledge that
              agriculture didn't get where it is today without advancements in the chemicals industry.
              """,
              'image': '/static/images/farm.jpg',
            },

#            {
#            'adjective': 'Spendthrift!',
#            'description': """Damn it, You are such a rich man. Go for Tesla S
#                """,
#            'image': '/static/images/buffett.jpg',
#            },
#
#            {
#            'adjective': 'You are miserly',
#            'description': """You would never spend on non-Migros Budget
#                products if you had a choice.
#                """,
#            'image': '/static/images/poorkids.png',
#            },

            {
            'adjective': 'You\'re a Xenophile!',
            'description': u""" 你係外国人来咯，唔晒埋瑞士货架!
                """,
            'image': '/static/images/eu.jpg',
            } if x[1] else \
            {
            'adjective': 'Ein stolzer Schweizer!',
            'description': u"""Du kauftest immer die Schweizer Produkte,
            auch wenn die Ausländische Produkte günstiger sind.
                """,
            'image': '/static/images/flag_switzerland.svg',
            },

            {
            'adjective': 'Du bist ein Treehugger',
            'description': u"""環境変化を気にしてツリーを抱きしめに外にアクセスしてください
                """,
            'image': '/static/images/treehugger.gif',
            } if x[3] else \
            {
            'adjective': 'You are Environmentally Indifferent',
            'description': """
                You couldn't care less if all the ice in Greenland
                and Antarctica melted tomorrow.
                Or you don't believe in climate change.
                Or both.
                """,
            'image': '/static/images/Igloo_landscape.svg',
            },
            ]
        }

    return render_template('results.html', **args)

if __name__ == '__main__':
    app.run()
