import os

from flask import Flask, request, redirect, url_for,\
	render_template
from werkzeug import secure_filename
import requests
import json


URL = 'http://text-processing.com/api/sentiment/'

ALLOWED_EXTENSIONS = set(['text', 'txt'])

app = Flask(__name__)
app.config['URL'] = URL

def allowed_file(filename):
    return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		type = request.form['button']

		fileitem = request.files.get('file',None)
		if type == "Submit":
			if file and allowed_file(fileitem.filename):
				filename = secure_filename(fileitem.filename)
				text = fileitem.stream.read()
				return render_template(
		        			"home.html",
		                 	text=text
							)
			else:
				return render_template('home.html',error="Invalid File format")
		elif type == "Analyse":
			text = str(request.form['textbox'])
			data = {'text': text}
			r = requests.post(URL, data=data)
			neg = r.json()['probability']['neg']
			pos = r.json()['probability']['pos']
			neutral = r.json()['probability']['neutral']
			label = r.json()['label']
			if label == "pos":
				label = "Positive"
			elif label == "neg":
				label = "Negative"
			elif label == "neutral":
				label = "Neutral"

			return render_template('home.html',text=text,neg=neg,pos=pos,neutral=neutral,label=label)
		else:
			return render_template('home.html')
	
	return render_template('home.html')



if __name__ == "__main__":
	app.run(debug=True)
