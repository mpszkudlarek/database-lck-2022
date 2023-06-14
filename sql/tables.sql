CREATE TABLE IF NOT EXISTS teams
(
    teams_id    BIGSERIAL PRIMARY KEY,
    team_name   VARCHAR(20) NOT NULL,
    player_top  VARCHAR(20) NOT NULL,
    player_jgl  VARCHAR(20) NOT NULL,
    player_mid  VARCHAR(20) NOT NULL,
    player_bot  VARCHAR(20) NOT NULL,
    player_supp VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS picks
(
    picks_id  BIGSERIAL PRIMARY KEY,
    pick_top  VARCHAR(20) NOT NULL,
    pick_jgl  VARCHAR(20) NOT NULL,
    pick_mid  VARCHAR(20) NOT NULL,
    pick_bot  VARCHAR(20) NOT NULL,
    pick_supp VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS bans
(
    bans_id BIGSERIAL PRIMARY KEY,
    ban_1   VARCHAR(20) NOT NULL,
    ban_2   VARCHAR(20) NOT NULL,
    ban_3   VARCHAR(20) NOT NULL,
    ban_4   VARCHAR(20) NOT NULL,
    ban_5   VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS games
(
    games_id         BIGSERIAL PRIMARY KEY,
    match_id         VARCHAR(100),
    match_date       DATE,
    game_number      INT,
    team_blue_ref_id BIGINT REFERENCES teams (teams_id),
    team_red_ref_id  BIGINT REFERENCES teams (teams_id),
    winner_ref_id    VARCHAR(20),
    pick_blue_ref_id BIGINT REFERENCES picks (picks_id),
    pick_red_ref_id  BIGINT REFERENCES picks (picks_id),
    ban_blue_ref_id  BIGINT REFERENCES bans (bans_id),
    ban_red_ref_id   BIGINT REFERENCES bans (bans_id)
);