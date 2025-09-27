INSERT INTO Users (email, name, password_hash) VALUES
('taha@gmail.com', 'taha', 'hashedpassword1')
('ahmed@gmail.com', 'ahmed', 'hashedpassword2')
('kamron@gmail.com', '', 'hashedpassword3')

INSERT INTO Organizers (user_id, club_name)
VALUES (2, 'Math Societe');

INSERT INTO Attendee (user_id, student_id)
VALUES 
  (1, '30008731'),
  (3, '30008742');


INSERT INTO Events (title, event_date, description, capacity)
VALUES ('AI and machine learning talk', '2025-10-15 19:00:00', 'discover the advancement of ai in the world', 45);

-- Link AHmed (organizer) to the event he created, function table
INSERT INTO Creates (event_id, user_id)
VALUES (1, 2);

-- Register Taha and kamron to the event
INSERT INTO Register_to (event_id, user_id)
VALUES (1, 1), (1, 3);