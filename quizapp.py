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

	if 'question_list' not in flask.session:
		flask.session['question_list'] = [] ## initialize this to a list of categories
	else:
		print 'Resued question list %s' % str(flask.session['question_list'])

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
	pass

if __name__ == '__main__':
	app.run()
