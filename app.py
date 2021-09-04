from flask import Flask, render_template
import os
import psycopg2

#DATABASE_URL = os.environ['DATABASE_URL']
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True)
