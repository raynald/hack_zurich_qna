#!/usr/bin/env python
# coding=utf-8
import migros
import flask
from flask import Flask
from flask import render_template, session, request

app = Flask(__name__)
app.debug = True
app.secret_key='this key is very secret indeed'

@app.route('/quiz')
def quiz():
	# Render the quiz start page
	return render_template('quiz.html')

@app.route('/question/<step>')
def question(step):
	"""
	Ask the user the question for this step
	"""

	if int(request.args['begin']):
		session.clear()

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
				session['answers'][qn_num] = 0
			elif request.args['clicked'] == 'right':
				session['answers'][qn_num] = 1
			else:
				session['answers'][qn_num] = None

	total_questions = len(flask.session['question_list'])
	args = {
			'image_left_source': 'http://migros-cache.fsi-viewer.com/fsicache/server?type=image&source=images%2Fmigros_api%2Fstaging%2Fproduct_204015800000.jpg',
			'image_right_source': 'http://migros-cache.fsi-viewer.com/fsicache/server?type=image&source=images%2Fmigros_api%2Fstaging%2Fproduct_204015800000.jpg',
			'statkeys': ['Fat', 'Sodium', 'Energy'],
			'leftstat': {'Fat': '100g', 'Sodium': '1mg', 'Energy': '1kcal'},
			'rightstat': {'Fat': '100g', 'Sodium': '1mg', 'Energy': '1kcal'},
			'question_num': step,
			'total_questions': 15,
			'form_action': '/question/%d' % (int(step)+1),
			};

	if step > total_questions:
		args['form_action'] = '/results'

	# Render the quiz start page
	return render_template('question.html', step=step, **args)

@app.route('/results')
def results():
	"""
	Give the user the results of the quiz
	"""

	user = None
	migros.SavePreferences( user, session['question_list'], session['answers'] )
	migros.PersonalityTest( session['question_list'], session['answers'] )

	args = {
		'enumerate': enumerate,
		'personality': [
			{
			'adjective': 'miserly',
			'description': """You would never spend on non-Migros Budget
				products if you had a choice.
				""",
			'image': '/static/images/poorkids.png',
			},

			{
			'adjective': 'proudly Swiss!',
			'description': u"""You kauftest immer die Schweizer Produkte,
			auch wenn die Ausländische Produkte günstiger sind.
				""",
			'image': '/static/images/flag_switzerland.svg',
			},

			{
			'adjective': 'Environmentally Indifferent!',
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
