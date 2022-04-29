SELECT *
FROM levelupapi_game_type;

drop table levelupapi_game;

insert into levelupapi_event (description, date, time, game_id, organizer_id)
values ('Online Caro','2022-1-1','12:00:00',2,1)