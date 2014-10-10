from flask import Flask
from flask import render_template


app = Flask(__name__)
app.debug = True

@app.route('/quiz')
def quiz():
	# Render the quiz start page
	return render_template('quiz.html')

if __name__ == '__main__':
	app.run()
