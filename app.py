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


# class Ban(db.Model):
#     __table_name__ = 'bans'

#     bans_id = db.Column(db.Integer, primary_key=True)
#     ban_1 = db.Column(db.String)
#     ban_2 = db.Column(db.String)
#     ban_3 = db.Column(db.String)
#     ban_4 = db.Column(db.String)
#     ban_5 = db.Column(db.String)

#     def to_dict(self):
#         return {
#             'bans_id': self.bans_id,
#             'ban_1': self.ban_1,
#             'ban_2': self.ban_2,
#             'ban_3': self.ban_3,
#             'ban_4': self.ban_4,
#             'ban_5': self.ban_5,
#         }

class Picks(db.Model):
    __tablename__ = 'picks'

    picks_id = db.Column(db.Integer, primary_key=True)
    pick_bot = db.Column(db.String)
    pick_jgl = db.Column(db.String)
    pick_mid = db.Column(db.String)
    pick_supp = db.Column(db.String)
    pick_top = db.Column(db.String)


class Ban(db.Model):
    __tablename__ = 'bans'

    bans_id = db.Column(db.Integer, primary_key=True)
    ban_1 = db.Column(db.String)
    ban_2 = db.Column(db.String)
    ban_3 = db.Column(db.String)
    ban_4 = db.Column(db.String)
    ban_5 = db.Column(db.String)


# class Games:
#     __tablename__ = 'games'
#     
#     games_id = db.Column(db.Integer, primary_key=True)
#     match

# @app.route('/champstats')
# def display_champstats():
#     champ_stats = {}
# 

class Teams(db.Model):
    __tablename_ = 'teams'

    teams_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String)
    player_top = db.Column(db.String)
    player_jgl = db.Column(db.String)
    player_mid = db.Column(db.String)
    player_bot = db.Column(db.String)
    player_supp = db.Column(db.String)


@app.route('/champstats')
def display_champstats():
    champion_stats = {}
    output = []
    all_picks = Picks.query.all()
    all_bans = Ban.query.all()
    total_picks = len(all_picks) / 2

    for pick in all_picks:
        for key in pick.__dict__.keys():
            if key.startswith('pick_'):
                champ = pick.__dict__[key]
                if champ in champion_stats:
                    champion_stats[champ]['pr'] += 1
                else:
                    champion_stats[champ] = {'pr': 1, 'br': 0}

    for ban in all_bans:
        for key in ban.__dict__.keys():
            if key.startswith('ban_'):
                champ = ban.__dict__[key]
                if champ in champion_stats:
                    champion_stats[champ]['br'] += 1
                else:
                    champion_stats[champ] = {'pr': 0, 'br': 1}

    for champ in champion_stats:
        pr = champion_stats[champ]['pr']
        br = champion_stats[champ]['br']
        wr = 'potem'
        presence = round((pr + br) / total_picks * 100, 2)
        presence_str = '{0:.2f}%'.format(presence)
        pr_str = '{0:.2f}%'.format(pr / total_picks * 100)
        br_str = '{0:.2f}%'.format(br / total_picks * 100)
        champion_stats[champ]['presence'] = presence_str
        champion_stats[champ]['pr'] = pr_str
        champion_stats[champ]['br'] = br_str
        champion_stats[champ]['championName'] = champ
        tmp = {'pr': pr, 'br': br, 'presence': presence, 'championName': champ}
        output.append(tmp)
    return jsonify(output)


# @app.route('/teamstats')
# def display_teamstats():
#     wins = 0
#     losses = 0
#     output = []
#     teams = []
#     picks = []
#     all_teams = Teams.query.all()
#     all_picks = Picks.query.all()
#     # creates all teams with players
#     for team in all_teams:
#         tmp = {'teamName': team.__dict__[team_name], 'playerTop': team.__dict__[player_top],
#                'playerJgl': team.__dict__[player_jgl],
#                'playerMid': team.__dict__[player_mid],
#                'playerBot': team.__dict__[player_bot],
#                'playerSupp': team.__dict__[player_supp],
#                'teamId': team.__dict__[teams_id]}
#         teams.append(tmp)
#     # now we need to do picks and win ratio
#     for game in all_games:
# 
#         for team in teams:
#             if (team['teamName'] == game.__dict__[winner_ref_id]):
#                 wins += 1;
#             else:
#                 losses += 1;
#             if (team['teamId'] == game.__dict__[team_blue_ref_id]):


# @app.route('/test')
# def display_data():
#     query = text("SELECT * FROM bans WHERE ban_1 LIKE 'A%'")
#     result = db.session.execute(query)
#     rows = result.fetchall()
# 
#     keys = result.keys()
#     results = [dict(zip(keys, row)) for row in rows]
# 
#     return jsonify(results)


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

#     cur = conn.cursor()
#     cur.execute("SELECT * FROM bans;")

#     rows = cur.fetchall()

#     cur.close()
#     conn.close()

#     results = []
#     for row in rows:
#         results.append({
#             'column1': row[0],
#             'column2': row[1]})
#     return jsonify(rows)

# if __name__ == '__main__':
#     app.run(debug=True)
