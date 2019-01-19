from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import json
import os

app = Flask(__name__, static_url_path='/static')

DB_FILE = "database.json"
HTML_TEMPLATE = "template.html"
PARAMETERS_IN_INFO = ["problem_type", "description", "example", "additional_resources", "image_url"]

if os.path.exists(DB_FILE) == False:
	os.system("echo [] >  {}".format(DB_FILE))

def create_db_backup():
	os.system("cp {} {}".format(DB_FILE, DB_FILE.partition(".")[0]+"_backup.json"))

def add_problem_to_file(data):
	if data != None:
		# This means the field had text before submission
		create_db_backup()
		a = json.load(open(DB_FILE))
		a.append(data)
		with open(DB_FILE, 'w') as outfile:
			json.dump(a, outfile)

def get_problem_type_info(problemType):
	return {'problemType': problemType}

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")


@app.route('/addProblem', methods=['POST'])
def add_problem():
	problem = request.form.get('problem', None)
	print problem
	add_problem_to_file(problem)
	# Adds the inputted problem to a file
	return ('', 204)

@app.route('/guide/<problemType>', methods=['GET'])
def get_guide(problemType):
	print os.listdir("./templates/")
	if os.path.exists("templates/{}.html".format(problemType)) == False:
		os.system("cp templates/{} templates/{}.html".format(HTML_TEMPLATE, problemType))
	return render_template("{}.html".format(problemType), info=get_problem_type_info(problemType))

@app.route('/getProblems', methods=['GET'])
def getProblems():
	a = json.load(open(DB_FILE))
	return jsonify(sorted(set(a), key=a.index))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
