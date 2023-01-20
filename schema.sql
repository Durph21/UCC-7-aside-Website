DROP TABLE IF EXISTS teams;

CREATE TABLE teams
(
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team TEXT NOT NULL,
    captain TEXT NOT NULL,
    points INTEGER NOT NULL,
    games played INTEGER NOT NULL
);

INSERT INTO teams (team, captain, points, games)
VALUES ('Clapped Niños Fc', 'Darragh Murphy', 21, '7'),
       ('North Park FC', 'Yinka', 18, 7),
       ('50 Shades of O Shea', 'Conor McNulty', 16, '7'),
       ('Parque De Bus', 'Matthew Sexton', 15, '7'),
       ('Pathetico Madrid', 'Eoin Clancy', 15, '7'),
       ('Air Fryer FC', 'Chris O Connell', 12, '7'),
       ('Pique Blinders', 'Cillian O Connor', 10, '6'),
       ('Boca Seniors', 'Tim Black', 9, '7'),
       ('Master Bakers', 'Jimmy Walsh', 7, '7'),
       ('Beamish FC', 'Mick Hennessy', 6, '7'),
       ('In Formation Systems', 'Lorcan Bridge', 4, '7'),
       ('Ha Mouldy Fc', 'Eoin Byrne', 3, '7'),
       ('Deans Hall', 'Mark Johnston', 18, '7'),
       ('Spice Boys', 'Pierce Reilly', 17, '6')
       ;


DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);


DROP TABLE IF EXISTS requests;

CREATE TABLE requests
(
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    team TEXT NOT NULL
);

DROP TABLE IF EXISTS admin;

CREATE TABLE admin
(
    admin_id TEXT PRIMARY KEY,
    admin_password TEXT NOT NULL
);

INSERT INTO admin (admin_id, admin_password)
VALUES ('ucc7aside', 'pbkdf2:sha256:260000$VA0wgGzK2kFuvyya$78f7fccb45505d100b6a886b5f5f2d2afe0f1cdb3b77ee97c3f26692d0b133c3');


DROP TABLE IF EXISTS players;

CREATE TABLE players
( 
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player TEXT NOT NULL,
    team TEXT NOT NULL
);

INSERT INTO players (team, player)
VALUES ('Clapped Niños Fc', 'Darragh Murphy'),
       ('North Park FC', 'Yinka'),
       ('50 Shades of O Shea', 'Conor McNulty'),
       ('Parque De Bus', 'Matthew Sexton'),
       ('Pathetico Madrid', 'Eoin Clancy'),
       ('Air Fryer FC', 'Chris O Connell'),
       ('Pique Blinders', 'Cillian O Connor'),
       ('Boca Seniors', 'Tim Black'),
       ('Master Bakers', 'Jimmy Walsh'),
       ('Beamish FC', 'Mick Hennessy'),
       ('In Formation Systems', 'Lorcan Bridge'),
       ('Ha Mouldy Fc', 'Eoin Byrne'),
       ('Deans Hall', 'Mark Johnston'),
       ('Spice Boys', 'Pierce Reilly');

SELECT *
FROM teams

SELECT *
FROM requests

SELECT *
FROM users

SELECT *
FROM players

SELECT player, team
FROM players
WHERE team = 'Clapped Niños Fc'
-- INSERT INTO players (team, player)
-- SELECT team, name 
-- FROM requests;

-- INSERT INTO players(team, player)
-- SELECT team, name 
-- FROM requests
-- WHERE player_id = ;

