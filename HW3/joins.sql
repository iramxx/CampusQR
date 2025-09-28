-- find the users that are also organizers

SELECT users.user_id, users.name, organizers.club_name
FROM users
JOIN organizers ON users.user_id = organizers.user_id
order by user_id
LIMIT 30


-- list all attendee and the events they are registered for
SELECT u.name AS attendee_name,e.title AS event_title
FROM Register_to AS rt
JOIN Users AS u ON rt.user_id = u.user_id
JOIN Events AS e ON rt.event_id = e.event_id;


-- find the events that are workshops

SELECT e.event_id, e.title, e.event_date, w.type
FROM Event e
JOIN Workshop w ON e.event_id = w.event_id;
