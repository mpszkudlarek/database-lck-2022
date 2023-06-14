import datetime
import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_PORT = '5432'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

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

w_dict = {
    1: '2022/06/15',
    2: '2022/06/21',
    3: '2022/06/28',
    4: '2022/07/05',
    5: '2022/07/12',
    6: '2022/07/19',
    7: '2022/07/26',
    8: '2022/08/02',
    9: '2022/08/09',
    10: '2022/08/15'

}


def check_week(date_to_check, dict_to_check):
    for i in range(1, 10):
        if dict_to_check[i] <= date_to_check <= dict_to_check[i + 1]:
            return 'W' + str(i)


def add_game(match_id, match_date, game_number, team_blue_ref_id, team_red_ref_id, winner_ref_id, pick_blue_ref_id,
             pick_red_ref_id, ban_blue_ref_id, ban_red_ref_id):
    cur.execute(
        f'INSERT INTO games(match_id,match_date, game_number, team_blue_ref_id, team_red_ref_id, winner_ref_id,'
        f' pick_blue_ref_id,'
        f'pick_red_ref_id,ban_blue_ref_id,'
        f'ban_red_ref_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (match_id, match_date, game_number, team_blue_ref_id, team_red_ref_id, winner_ref_id, pick_blue_ref_id,
         pick_red_ref_id, ban_blue_ref_id, ban_red_ref_id))
    conn.commit()


def add_picks(pick_top, pick_jgl, pick_mid, pick_bot, pick_supp):
    cur.execute(f'INSERT INTO picks(pick_top, pick_jgl, pick_mid, pick_bot, pick_supp) VALUES (%s,%s,%s,%s,%s)',
                (pick_top, pick_jgl, pick_mid, pick_bot, pick_supp))
    conn.commit()


def add_bans(ban_1, ban_2, ban_3, ban_4, ban_5):
    cur.execute(f'INSERT INTO bans(ban_1, ban_2, ban_3, ban_4, ban_5) VALUES (%s,%s,%s,%s,%s)',
                (ban_1, ban_2, ban_3, ban_4, ban_5))
    conn.commit()


def add_player(team_name, player_top, player_jgl, player_mid, player_bot, player_supp):
    cur.execute(
        f'INSERT INTO teams(team_name, player_top, player_jgl, player_mid,player_bot, player_supp) VALUES (%s,%s,%s,%s,%s,%s)',
        (team_name, player_top, player_jgl, player_mid, player_bot, player_supp))
    conn.commit()


with open('matches.csv', 'r') as f:
    next(f)
    game_counter = 1
    previous_blue_team = None
    previous_red_team = None
    ref_id = 1
    for s in f:
        s = s.strip()
        dateText, blueTeamName, redTeamName, winnerName, blueBan1, blueBan2, blueBan3, blueBan4, blueBan5, \
            redBan1, redBan2, redBan3, redBan4, redBan5, bluePick1, bluePick2, bluePick3, bluePick4, bluePick5, \
            redPick1, redPick2, redPick3, redPick4, redPick5, blueTop, blueJng, blueMid, blueAdc, blueSup, redTop, \
            redJng, redMid, redAdc, redSup = s.split(',')

        if (previous_blue_team == blueTeamName and previous_red_team == redTeamName) or (
                previous_blue_team == redTeamName and previous_red_team == blueTeamName):
            game_counter += 1
        else:
            game_counter = 1

        previous_red_team = redTeamName
        previous_blue_team = blueTeamName

        date = datetime.datetime.strptime(dateText, '%m/%d/%Y').date()
        date_str = date.strftime('%Y/%m/%d')
        week = check_week(date_str, w_dict)

        match_id_name = 'SUM22_' + week + 'G' + str(game_counter) + '_' + \
                        teams_dict[blueTeamName] + '_' + teams_dict[redTeamName]

        add_bans(blueBan1, blueBan2, blueBan3, blueBan4, blueBan5)
        blue_ban_id = ref_id
        add_bans(redBan1, redBan2, redBan3, redBan4, redBan5)
        red_ban_id = ref_id + 1

        add_player(blueTeamName, blueTop, blueJng, blueMid, blueAdc, blueSup)
        blue_roster_id = ref_id
        add_player(redTeamName, redTop, redJng, redMid, redAdc, redSup)
        red_roster_id = ref_id + 1

        add_picks(bluePick1, bluePick2, bluePick3, bluePick4, bluePick5)
        blue_pick_id = ref_id
        add_picks(redPick1, redPick2, redPick3, redPick4, redPick5)
        red_pick_id = ref_id + 1

        add_game(match_id_name, date, game_counter, blue_roster_id, red_roster_id, winnerName, blue_pick_id,
                 red_pick_id, blue_ban_id, red_ban_id)
        ref_id = ref_id + 2

cur.close()
conn.close()
