

Create Table 'Users' (
 'user_id' INT NOT NULL AUTO_INCREMENT,
 'email' VARCHAR(255) NOT NULL,
 'name' VARCHAR(255) NOT NULL,
 'password_hash' VARCHAR(255) NOT NULL,
 PRIMARY KEY('user_id')
);


Create table 'Events' (
 'event_id' INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 'title' VARCHAR(255) NOT NULL,
 'event_date' DATETIME NOT NULL,
 'description' TEXT NOT NULL,
 'capacity' INT UNSIGNED NOT NULL,
)


CREATE TABLE Tickets (
 ticket_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 status ENUM('issued', 'checked_in', 'cancelled') NOT NULL DEFAULT 'issued',
 qr_code_data VARCHAR(255) NOT NULL
);


CREATE TABLE Organizers (
 user_id INT UNSIGNED NOT NULL AUTO_INCREMENT  PRIMARY KEY,
 club_name VARCHAR(255) NOT NULL,
 FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);


CREATE TABLE Attendee (
user_id INT UNSIGNED NOT NULL AUTO_INCREMENT  PRIMARY KEY,
 student_id VARCHAR(255) NOT NULL,
FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);








CREATE TABLE Creates (
 event_id INT USIGNED NOT NULL AUTO_INCREMENT ,
 user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
PRIMARY KEY (event_id, user_id),
 FOREIGN KEY (event_id) REFERENCES Events,
FOREIGN KEY (user_id) REFERENCES Organizers
);


CREATE TABLE Register_to (
 event_id INT USIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
PRIMARY KEY (event_id, user_id),
 FOREIGN KEY (event_id) REFERENCES Events,
FOREIGN KEY (user_id) REFERENCES Attendee
);




CREATE TABLE Scans (
 ticket_id INT USIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
PRIMARY KEY (ticket_id, user_id),
 FOREIGN KEY (ticket_id) REFERENCES Tickets,
FOREIGN KEY (user_id) REFERENCES Organizers






);




CREATE TABLE Generates (
 event_id INT USIGNED NOT NULL,
 ticket_id INT UNSIGNED NOT NULL,
PRIMARY KEY (ticket_id, event_id),
 FOREIGN KEY (ticket_id) REFERENCES Tickets,
FOREIGN KEY (event_id) REFERENCES Events
);








CREATE TABLE StudentTicket (
 user_id INT UNSIGNED NOT NULL AUTO_INCREMENT  PRIMARY KEY,
booking_date DATETIME NOT NULL
);







