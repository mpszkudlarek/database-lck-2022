import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)
db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'postgres')
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'postgres')
db_port = os.environ.get('DB_PORT', '5432')


@app.route('/')
def siemanko():
    return 'Siemanko, witam w mojej kuchni!'


@app.route('/test')
def display_data():
    # Establish a connection to the database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM bans;")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []
    for row in rows:
        results.append({
            'column1': row[0],
            'column2': row[1]})
    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True)
