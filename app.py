from flask import Flask, render_template
import psycopg2

DATABASE_URL = "dbname=duke-of-e-database user=postgres password=9jl2$*gsi96*h8AjpdZ71 port=9261"
conn = psycopg2.connect(DATABASE_URL)
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True)
