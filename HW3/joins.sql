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

-- How many users to we have
SELECT COUNT(*) AS total_users
FROM User;

-- How many tickets to we have
SELECT COUNT(*) AS total_tickets
FROM Ticket;
-- Find all events after specific date
SELECT title, event_date,capacity
FROM Events
WHERE event_date > '2025-01-01 00:00:00';

-- Attendees who are not registered to any events
SELECT u.name, u.email
FROM Attendee AS a
JOIN Users AS u ON a.user_id = u.user_id
WHERE a.user_id NOT IN (SELECT user_id FROM Register_to)

-- Print all users in alphabetic order
SELECT user_id, name, email
FROM Users
ORDER BY name ASC;

SELECT tickets.status, COUNT(*)
FROM tickets
GROUP BY tickets.status

