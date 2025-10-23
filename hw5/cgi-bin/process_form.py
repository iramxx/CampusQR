#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable() # ОБЯЗАТЕЛЬНО для отладки

import cgi
import mysql.connector
from mysql.connector import Error
import hashlib
import os
import uuid

# --- КОНФИГУРАЦИЯ ---
db_config = { 'host': 'clabsql', 'database': 'db_kjurabaev', 'user': 'kjurabaev', 'password': '5tr8zjbrDq1GchfY' }
username = os.environ.get('USER', 'kjurabaev')

# --- ФУНКЦИИ-ПОМОЩНИКИ ---
def print_feedback_page(success, message):
    print("Content-Type: text/html\n")
    print(f"<html><head><title>Feedback</title><link rel='stylesheet' href='/~{username}/auth-style.css'></head><body>")
    print('<div class="auth-container"><div class="form-container">')
    print(f"<h2>{'Success!' if success else 'Error!'}</h2><p>{message}</p>")
    print(f'<a href="/~{username}/maintenance.html" class="back-link">← Back to Maintenance</a>')
    print("</div></div></body></html>")

# --- ОСНОВНАЯ ЛОГИКА ---
def main():
    form = cgi.FieldStorage()
    action = form.getvalue('action')
    msg = ""
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # --- ОБРАБОТКА СУЩНОСТЕЙ ---
        if action == 'add_user':
            password_hash = hashlib.sha256(form.getvalue('password').encode('utf-8')).hexdigest()
            cursor.execute("INSERT INTO Users (name, email, password_hash) VALUES (%s, %s, %s)",
                           (form.getvalue('name'), form.getvalue('email'), password_hash))
            msg = "User added successfully."

        elif action == 'add_talk':
            cursor.execute("INSERT INTO Events (title, event_date, description, capacity, speaker_name, event_type) VALUES (%s, %s, %s, %s, %s, 'Talk')",
                           (form.getvalue('title'), form.getvalue('event_date'), form.getvalue('description'), form.getvalue('capacity'), form.getvalue('speaker_name')))
            msg = "Talk event added successfully."

        elif action == 'add_workshop':
            cursor.execute("INSERT INTO Events (title, event_date, description, capacity, event_type) VALUES (%s, %s, %s, %s, %s)",
                           (form.getvalue('title'), form.getvalue('event_date'), form.getvalue('description'), form.getvalue('capacity'), form.getvalue('event_type')))
            msg = "Workshop event added successfully."

        elif action == 'add_organizer':
            cursor.execute("INSERT INTO Organizers (user_id, club_name) VALUES (%s, %s)",
                           (form.getvalue('user_id'), form.getvalue('club_name')))
            msg = "Organizer profile created."

        elif action == 'add_attendee':
            cursor.execute("INSERT INTO Attendee (user_id, student_id) VALUES (%s, %s)",
                           (form.getvalue('user_id'), form.getvalue('student_id')))
            msg = "Attendee profile created."

        elif action == 'add_ticket':
            qr_code = str(uuid.uuid4())
            cursor.execute("INSERT INTO Tickets (status, qr_code_data) VALUES ('issued', %s)", (qr_code,))
            ticket_id = cursor.lastrowid
            # В зависимости от твоей SQL схемы, ты можешь вставлять в StudentTicket или GuestTicket
            # Для примера, вставляем в StudentTicket
            cursor.execute("INSERT INTO StudentTicket (user_id, ticket_id, booking_date) VALUES (%s, %s, NOW())",
                           (form.getvalue('user_id'), ticket_id))
            msg = f"Ticket created with ID {ticket_id}."

        # --- ОБРАБОТКА СВЯЗЕЙ ---
        elif action == 'link_creates':
            cursor.execute("INSERT INTO Creates (user_id, event_id) VALUES (%s, %s)",
                           (form.getvalue('user_id'), form.getvalue('event_id')))
            msg = "Organizer linked to Event."

        elif action == 'link_register_to':
            cursor.execute("INSERT INTO Register_to (user_id, event_id) VALUES (%s, %s)",
                           (form.getvalue('user_id'), form.getvalue('event_id')))
            msg = "Attendee registered for Event."

        elif action == 'link_scans':
            ticket_id = form.getvalue('ticket_id')
            cursor.execute("UPDATE Tickets SET status = 'checked_in' WHERE ticket_id = %s", (ticket_id,))
            cursor.execute("INSERT INTO Scans (user_id, ticket_id) VALUES (%s, %s)",
                           (form.getvalue('user_id'), ticket_id))
            msg = "Ticket scanned successfully."
            
        else:
            raise ValueError("Invalid action specified.")

        conn.commit()
        print_feedback_page(True, msg)

    except (Error, ValueError, TypeError) as e:
        if "Duplicate entry" in str(e):
            print_feedback_page(False, "This link or role already exists.")
        else:
            print_feedback_page(False, str(e))
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()