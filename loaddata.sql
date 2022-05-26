SELECT *
FROM levelupapi_game_type;

drop table levelupapi_game;

insert into levelupapi_event (description, date, time, game_id, organizer_id)
values ('Online Caro II','2022-1-1','12:00:00',2,2)

update levelupapi_event
set organizer_id = 2
where id in (3,5);

update levelupapi_game
set gamer_id = 2
where id in (2,4)

-- user_games list
SELECT
    g.title as "Title", gm.id as "gamer_id",
    au.first_name || " " || au.last_name AS "full_name"
FROM levelupapi_game g
JOIN levelupapi_gamer gm
    ON g.gamer_id = gm.id
JOIN auth_user au
    ON gm.user_id = au.id

-- gamer_event list
SELECT
    g.title AS game_title, e.description AS event_description,
    e.date, e.time, gm.id AS gamer_id,
    au.first_name || " " || au.last_name AS "gamer_full_name"
FROM levelupapi_gamer gm
JOIN levelupapi_game g
    ON gm.id = g.gamer_id
JOIN levelupapi_event e
    ON e.game_id = g.id
JOIN auth_user au
    ON au.id = gm.user_id
ORDER BY gamer_full_name