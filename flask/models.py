from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


class Games(db.Model):
    __tablename__ = 'games'

    games_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String)
    match_date = db.Column(db.String)
    game_number = db.Column(db.Integer)
    team_blue_ref_id = db.Column(db.Integer)
    team_red_ref_id = db.Column(db.Integer)
    winner_ref_id = db.Column(db.String)
    pick_blue_ref_id = db.Column(db.Integer)
    pick_red_ref_id = db.Column(db.Integer)
    ban_blue_ref_id = db.Column(db.Integer)
    ban_red_ref_id = db.Column(db.Integer)


class Teams(db.Model):
    __tablename_ = 'teams'

    teams_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String)
    player_top = db.Column(db.String)
    player_jgl = db.Column(db.String)
    player_mid = db.Column(db.String)
    player_bot = db.Column(db.String)
    player_supp = db.Column(db.String)
