from flask import flask

app = Flask(__name__)



@app.route('/')
def home():
    return 'fuck me'


app.run(debug=True)
