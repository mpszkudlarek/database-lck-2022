# import os
# from collections import namedtuple
# import psycopg2
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)


class Ban(db.Model):
    __table_name__ = 'bans'

    bans_id = db.Column(db.Integer, primary_key=True)
    ban_1 = db.Column(db.String)
    ban_2 = db.Column(db.String)
    ban_3 = db.Column(db.String)
    ban_4 = db.Column(db.String)
    ban_5 = db.Column(db.String)

    def to_dict(self):
        return {
            'bans_id': self.bans_id,
            'ban_1': self.ban_1,
            'ban_2': self.ban_2,
            'ban_3': self.ban_3,
            'ban_4': self.ban_4,
            'ban_5': self.ban_5,
        }


@app.route('/test')
def display_data():
    query = text("SELECT * FROM bans WHERE ban_1 LIKE 'A%'")
    result = db.session.execute(query)
    rows = result.fetchall()

    keys = result.keys()
    results = [dict(zip(keys, row)) for row in rows]

    return jsonify(results)


# app = Flask(__name__)
# db_host = os.environ.get('DB_HOST', 'localhost')
# db_name = os.environ.get('DB_NAME', 'postgres')
# db_user = os.environ.get('DB_USER', 'postgres')
# db_password = os.environ.get('DB_PASSWORD', 'postgres')
# db_port = os.environ.get('DB_PORT', '5432')
@app.route('/')
def siemanko():
    return 'Siemanko, witam w mojej kuchni!'


if __name__ == '__main__':
    app.run(debug=True)
# @app.route('/test')
# def display_data():
# Establish a connection to the database
#     conn = psycopg2.connect(
#         host=db_host,
#         port=db_port,
#         dbname=db_name,
#         user=db_user,
#         password=db_password
#     )
# 
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM bans;")
# 
#     rows = cur.fetchall()
# 
#     cur.close()
#     conn.close()
# 
#     results = []
#     for row in rows:
#         results.append({
#             'column1': row[0],
#             'column2': row[1]})
#     return jsonify(rows)
# 
# 
# if __name__ == '__main__':
#     app.run(debug=True)
