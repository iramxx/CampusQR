-- find the users that are also organizers

SELECT users.user_id, users.name, organizers.club_name
FROM users
JOIN organizers ON users.user_id = organizers.user_id
order by user_id
LIMIT 30




