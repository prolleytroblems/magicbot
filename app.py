from flask import Flask

app = Flask(__name__)



@app.route('/')
def home():
    return 'fuck me'


app.run(port=5000)
