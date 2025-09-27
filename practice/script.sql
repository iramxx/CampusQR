INSERT INTO Users (email, name, password_hash) VALUES
('taha1@mail.com', 'Taha', 'hash1'),
('ahmed@mail.com', 'Ahmed', 'hash2'),
('kamron@mail.com', 'Kamron', 'hash3'),
('sara@mail.com', 'Sara', 'hash4'),
('ali@mail.com', 'Ali', 'hash5'),
('fatima@mail.com', 'Fatima', 'hash6'),
('youssef@mail.com', 'Youssef', 'hash7'),
('mohammed@mail.com', 'Mohammed', 'hash8'),
('nour@mail.com', 'Nour', 'hash9'),
('amina@mail.com', 'Amina', 'hash10'),
('hassan@mail.com', 'Hassan', 'hash11'),
('iman@mail.com', 'Iman', 'hash12'),
('khalid@mail.com', 'Khalid', 'hash13'),
('salma@mail.com', 'Salma', 'hash14'),
('omar@mail.com', 'Omar', 'hash15'),
('yasin@mail.com', 'Yasin', 'hash16'),
('hanan@mail.com', 'Hanan', 'hash17'),
('adil@mail.com', 'Adil', 'hash18'),
('ranya@mail.com', 'Ranya', 'hash19'),
('karim@mail.com', 'Karim', 'hash20'),
('layla@mail.com', 'Layla', 'hash21'),
('reda@mail.com', 'Reda', 'hash22'),
('nadia@mail.com', 'Nadia', 'hash23'),
('samir@mail.com', 'Samir', 'hash24'),
('siham@mail.com', 'Siham', 'hash25'),
('yara@mail.com', 'Yara', 'hash26'),
('mehdi@mail.com', 'Mehdi', 'hash27'),
('aya@mail.com', 'Aya', 'hash28'),
('zakaria@mail.com', 'Zakaria', 'hash29'),
('mona@mail.com', 'Mona', 'hash30');


INSERT INTO Organizers (user_id, club_name)
VALUES
  (2, 'Math Societe'),
  (8, 'Chess Club'),
  (10, 'Debate Club'),
  (29, 'Photography Club');


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