CREATE TABLE Users (
  user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  PRIMARY KEY(user_id)
);

CREATE TABLE Events (
  event_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  event_date DATETIME NOT NULL,
  description TEXT NOT NULL,
  capacity INT UNSIGNED NOT NULL,
  PRIMARY KEY(event_id)
);

CREATE TABLE Tickets (
  ticket_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  status ENUM('issued', 'checked_in', 'cancelled') NOT NULL DEFAULT 'issued',
  qr_code_data VARCHAR(255) NOT NULL,
  PRIMARY KEY(ticket_id)
);

CREATE TABLE Organizers (
  user_id INT UNSIGNED NOT NULL,
  club_name VARCHAR(255) NOT NULL,
  PRIMARY KEY(user_id),
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Attendee (
  user_id INT UNSIGNED NOT NULL,
  student_id VARCHAR(255) NOT NULL,
  PRIMARY KEY(user_id),
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Creates (
  event_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (event_id, user_id),
  FOREIGN KEY (event_id) REFERENCES Events(event_id),
  FOREIGN KEY (user_id) REFERENCES Organizers(user_id)
);

CREATE TABLE Register_to (
  event_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (event_id, user_id),
  FOREIGN KEY (event_id) REFERENCES Events(event_id),
  FOREIGN KEY (user_id) REFERENCES Attendee(user_id)
);

CREATE TABLE Scans (
  ticket_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (ticket_id, user_id),
  FOREIGN KEY (ticket_id) REFERENCES Tickets(ticket_id),
  FOREIGN KEY (user_id) REFERENCES Organizers(user_id)
);

CREATE TABLE Generates (
  event_id INT UNSIGNED NOT NULL,
  ticket_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (ticket_id, event_id),
  FOREIGN KEY (ticket_id) REFERENCES Tickets(ticket_id),
  FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE StudentTicket (
  user_id INT UNSIGNED NOT NULL,
  ticket_id INT UNSIGNED NOT NULL,
  booking_date DATETIME NOT NULL,
  PRIMARY KEY (user_id, ticket_id),
  FOREIGN KEY (user_id) REFERENCES Users(user_id),
  FOREIGN KEY (ticket_id) REFERENCES Tickets(ticket_id)
);
