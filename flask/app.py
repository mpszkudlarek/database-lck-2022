from collections import defaultdict

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)


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


@app.route('/winratio')
def display_winrate():
    pick_win_count = defaultdict(int)
    pick_total_count = defaultdict(int)
    all_games = Games.query.all()

    for game in all_games:
        pick_blue = Picks.query.get(game.pick_blue_ref_id)
        pick_red = Picks.query.get(game.pick_red_ref_id)

        blue_team = Teams.query.filter_by(teams_id=game.team_blue_ref_id).first()

        if game.winner_ref_id == blue_team.team_name:
            winning_pick = pick_blue
        else:
            winning_pick = pick_red

        pick_win_count[winning_pick.pick_top] += 1
        pick_win_count[winning_pick.pick_jgl] += 1
        pick_win_count[winning_pick.pick_mid] += 1
        pick_win_count[winning_pick.pick_bot] += 1
        pick_win_count[winning_pick.pick_supp] += 1

        pick_total_count[pick_blue.pick_top] += 1
        pick_total_count[pick_blue.pick_jgl] += 1
        pick_total_count[pick_blue.pick_mid] += 1
        pick_total_count[pick_blue.pick_bot] += 1
        pick_total_count[pick_blue.pick_supp] += 1

        pick_total_count[pick_red.pick_top] += 1
        pick_total_count[pick_red.pick_jgl] += 1
        pick_total_count[pick_red.pick_mid] += 1
        pick_total_count[pick_red.pick_bot] += 1
        pick_total_count[pick_red.pick_supp] += 1

    pick_win_ratio = {}
    for champ in pick_total_count.keys():
        win_count = pick_win_count[champ]
        total_count = pick_total_count[champ]
        win_ratio = win_count / total_count * 100
        win_ratio_str = '{0:.2f}%'.format(win_ratio)
        pick_win_ratio[champ] = {'win_ratio': win_ratio_str}

    return jsonify(pick_win_ratio)


@app.route('/alldata')
def display_alldata():
    game_data = []

    all_games = Games.query.all()

    for game in all_games:
        match_date = game.match_date.strftime("%Y-%m-%d")

        blue_team = Teams.query.get(game.team_blue_ref_id)
        red_team = Teams.query.get(game.team_red_ref_id)
        winner_team = Teams.query.filter_by(team_name=game.winner_ref_id).first()

        ban_blue = Ban.query.get(game.ban_blue_ref_id)
        ban_red = Ban.query.get(game.ban_red_ref_id)

        pick_blue = Picks.query.get(game.pick_blue_ref_id)
        pick_red = Picks.query.get(game.pick_red_ref_id)

        game_info = {
            'match_date': match_date,
            'blue_team_name': blue_team.team_name,
            'blue_player_top': blue_team.player_top,
            'blue_player_jungle': blue_team.player_jgl,
            'blue_player_mid': blue_team.player_mid,
            'blue_player_bot': blue_team.player_bot,
            'blue_player_support': blue_team.player_supp,
            'ban_blue1': ban_blue.ban_1,
            'ban_blue2': ban_blue.ban_2,
            'ban_blue3': ban_blue.ban_3,
            'ban_blue4': ban_blue.ban_4,
            'ban_blue5': ban_blue.ban_5,
            'pick_blue1': pick_blue.pick_top,
            'pick_blue2': pick_blue.pick_jgl,
            'pick_blue3': pick_blue.pick_mid,
            'pick_blue4': pick_blue.pick_bot,
            'pick_blue5': pick_blue.pick_supp,

            'red_team_name': red_team.team_name,
            'red_player_top': red_team.player_top,
            'red_player_jungle': red_team.player_jgl,
            'red_player_mid': red_team.player_mid,
            'red_player_bot': red_team.player_bot,
            'red_player_support': red_team.player_supp,

            'ban_red1': ban_red.ban_1,
            'ban_red2': ban_red.ban_2,
            'ban_red3': ban_red.ban_3,
            'ban_red4': ban_red.ban_4,
            'ban_red5': ban_red.ban_5,

            'pick_red1': pick_red.pick_top,
            'pick_red2': pick_red.pick_jgl,
            'pick_red3': pick_red.pick_mid,
            'pick_red4': pick_red.pick_bot,
            'pick_red5': pick_red.pick_supp,

            'winner_team': winner_team.team_name
        }

        game_data.append(game_info)

    output_json = jsonify(game_data)
    output_json.headers.add('Access-Control-Allow-Origin', '*')
    return output_json


@app.route('/sidewinrate')
def display_side_winrate():
    blue_wins = 0
    red_wins = 0
    all_games = Games.query.all()

    for game in all_games:
        blue_team = Teams.query.filter_by(teams_id=game.team_blue_ref_id, team_name=game.winner_ref_id).first()
        red_team = Teams.query.filter_by(teams_id=game.team_red_ref_id, team_name=game.winner_ref_id).first()

        if blue_team:
            blue_wins += 1
        elif red_team:
            red_wins += 1

    total_games = blue_wins + red_wins
    blue_win_rate = round(blue_wins / total_games * 100, 2)
    red_win_rate = round(red_wins / total_games * 100, 2)

    output = {'blue': blue_win_rate, 'red': red_win_rate}

    output_json = jsonify(output)
    output_json.headers.add('Access-Control-Allow-Origin', '*')
    return output_json


@app.route('/champstats')
def display_champ_stats():
    champion_stats = {}
    output = []
    all_picks = Picks.query.all()
    all_bans = Ban.query.all()
    total_picks = len(all_picks) / 2

    pick_win_ratio = display_winrate().json

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
        wr = pick_win_ratio.get(champ, {}).get('win_ratio')
        presence = round((pr + br) / total_picks * 100, 2)
        presence_str = '{0:.2f}%'.format(presence)
        champion_stats[champ]['championName'] = champ
        tmp = {'pr': pr, 'br': br, 'presence': presence_str, 'championName': champ, 'wr': wr}
        output.append(tmp)

    output_json = jsonify(output)
    output_json.headers.add('Access-Control-Allow-Origin', '*')
    return output_json


teams_dict = {
    'Gen.G': 'GEN',
    'T1': 'T1',
    'Liiv SANDBOX': 'LSB',
    'DWG KIA': 'DK',
    'KT Rolster': 'KT',
    'DRX': 'DRX',
    'Kwangdong Freecs': 'KDF',
    'Nongshim RedForce': 'NS',
    'Fredit BRION': 'BRO',
    'Hanwha Life Esports': 'HLE'
}


@app.route('/teamstats')
def display_teamstats():
    team_stats = {}
    all_games = Games.query.all()

    for game in all_games:
        team_blue = Teams.query.get(game.team_blue_ref_id)
        team_red = Teams.query.get(game.team_red_ref_id)

        if team_blue.team_name not in team_stats:
            team_stats[team_blue.team_name] = {
                'team_name': teams_dict[team_blue.team_name],
                'wins': 0,
                'total_games': 0,
                'win_ratio': 0
            }

        if team_red.team_name not in team_stats:
            team_stats[team_red.team_name] = {
                'team_name': teams_dict[team_red.team_name],
                'wins': 0,
                'total_games': 0,
                'win_ratio': 0
            }

        team_stats[team_blue.team_name]['total_games'] += 1
        team_stats[team_red.team_name]['total_games'] += 1

        if game.winner_ref_id == team_blue.team_name:
            team_stats[team_blue.team_name]['wins'] += 1
        elif game.winner_ref_id == team_red.team_name:
            team_stats[team_red.team_name]['wins'] += 1

    output = []
    for team_name, stats in team_stats.items():
        wins = stats['wins']
        total_games = stats['total_games']
        win_ratio = wins / total_games if total_games > 0 else 0
        win_ratio_string = '{0:.2f}%'.format(win_ratio * 100)

        team_data = {
            'team_name': team_name,
            'wins': wins,
            'loses': total_games - wins,
            'total_games': total_games,
            'win_ratio': win_ratio_string
        }

        player_details = Teams.query.filter_by(team_name=team_name).first()
        if player_details:
            team_data.update({
                'player_top': player_details.player_top,
                'player_jungle': player_details.player_jgl,
                'player_mid': player_details.player_mid,
                'player_bot': player_details.player_bot,
                'player_support': player_details.player_supp
            })

        output.append(team_data)

    output_json = jsonify(output)
    output_json.headers.add('Access-Control-Allow-Origin', '*')
    return output_json


@app.route('/')
def home_page():
    return 'Siemanko, witam w mojej kuchni!'


if __name__ == '__main__':
    app.run(debug=True)
