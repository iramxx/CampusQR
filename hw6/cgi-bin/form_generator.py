#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

import cgi
import mysql.connector
from mysql.connector import Error
import os

# --- КОНФИГУРАЦИЯ (Убедись, что пароль верный) ---
db_config = { 'host': 'localhost', 'database': 'db_kjurabaev', 'user': 'kjurabaev', 'password': '5tr8zjbrDq1GchfY' }
username = os.environ.get('USER', 'kjurabaev')


# --- ФУНКЦИИ-ПОМОЩНИКИ ---
def print_html_header(title):
    # Эта функция теперь вызывается ПОСЛЕ подключения к БД, поэтому она должна печатать заголовок
    print("Content-Type: text/html\n")
    print(f"<html><head><title>{title}</title><link rel='stylesheet' href='/~{username}/auth-style.css'></head><body>")
    print(f"<div class='auth-container'><div class='form-container'><h2>{title}</h2>")

def print_html_footer():
    print(f"<a href='/~{username}/maintenance.html' class='back-link'>← Back to Maintenance</a></div></div></body></html>")

def get_select_options(cursor, query):
    cursor.execute(query)
    items = cursor.fetchall()
    options = ""
    for item in items:
        options += f"<option value='{item[0]}'>{item[1]}</option>\n"
    return options

# --- ОСНОВНАЯ ЛОГИКА ---
def main():
    # Сначала пробуем подключиться к БД. Если не получится, скрипт упадет и cgitb покажет ошибку.
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Если подключение успешно, читаем параметры формы
    form_data = cgi.FieldStorage()
    form_type = form_data.getvalue('form')

    # Теперь, когда все готово, печатаем заголовок
    # (Название страницы будет зависеть от типа формы)
    page_titles = {
        'add_user': "Add New User",
        'add_organizer': "Create Organizer Profile",
        'add_attendee': "Create Attendee Profile",
        'add_ticket': "Create Student/Guest Ticket",
        'link_creates': "Link Organizer to Event (Creates)",
        'link_register_to': "Register Attendee for Event",
        'link_scans': "Scan a Ticket"
    }
    page_title = page_titles.get(form_type, "Error")
    print_html_header(page_title)

    # Генерируем нужную форму
    if form_type == 'add_user':
        print('<form action="process_form.py?action=add_user" method="POST">')
        print('<div class="form-group"><input type="text" name="name" required placeholder="User Name"></div>')
        print('<div class="form-group"><input type="email" name="email" required placeholder="User Email"></div>')
        print('<div class="form-group"><input type="password" name="password" required placeholder="Password"></div>')
        print('<button type="submit" class="btn-submit">Add User</button></form>')

    elif form_type == 'add_organizer':
        options = get_select_options(cursor, "SELECT user_id, name FROM Users WHERE user_id NOT IN (SELECT user_id FROM Organizers)")
        print('<form action="process_form.py?action=add_organizer" method="POST">')
        print(f'<div class="form-group"><label>Select User:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<div class="form-group"><input type="text" name="club_name" required placeholder="Club Name"></div>')
        print('<button type="submit" class="btn-submit">Create Profile</button></form>')

    elif form_type == 'add_attendee':
        options = get_select_options(cursor, "SELECT user_id, name FROM Users WHERE user_id NOT IN (SELECT user_id FROM Attendee)")
        print('<form action="process_form.py?action=add_attendee" method="POST">')
        print(f'<div class="form-group"><label>Select User:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<div class="form-group"><input type="text" name="student_id" required placeholder="Student ID"></div>')
        print('<button type="submit" class="btn-submit">Create Profile</button></form>')

    elif form_type == 'add_ticket':
        options = get_select_options(cursor, "SELECT user_id, name FROM Users")
        print('<form action="process_form.py?action=add_ticket" method="POST">')
        print(f'<div class="form-group"><label>Assign ticket to User:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<button type="submit" class="btn-submit">Create Ticket</button></form>')
    
    elif form_type == 'link_creates':
        org_options = get_select_options(cursor, "SELECT U.user_id, U.name FROM Users U JOIN Organizers O ON U.user_id = O.user_id")
        evt_options = get_select_options(cursor, "SELECT event_id, title FROM Events")
        print('<form action="process_form.py?action=link_creates" method="POST">')
        print(f'<div class="form-group"><label>Organizer:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{org_options}</select></div>')
        print(f'<div class="form-group"><label>Event:</label><select name="event_id" class="form-group" style="width:100%; padding:15px;">{evt_options}</select></div>')
        print('<button type="submit" class="btn-submit">Link</button></form>')

    elif form_type == 'link_register_to':
        att_options = get_select_options(cursor, "SELECT U.user_id, U.name FROM Users U JOIN Attendee A ON U.user_id = A.user_id")
        evt_options = get_select_options(cursor, "SELECT event_id, title FROM Events")
        print('<form action="process_form.py?action=link_register_to" method="POST">')
        print(f'<div class="form-group"><label>Attendee:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{att_options}</select></div>')
        print(f'<div class="form-group"><label>Event:</label><select name="event_id" class="form-group" style="width:100%; padding:15px;">{evt_options}</select></div>')
        print('<button type="submit" class="btn-submit">Register</button></form>')

    elif form_type == 'link_scans':
        org_options = get_select_options(cursor, "SELECT U.user_id, U.name FROM Users U JOIN Organizers O ON U.user_id = O.user_id")
        tkt_options = get_select_options(cursor, "SELECT ticket_id, qr_code_data FROM Tickets WHERE status = 'issued'")
        print('<form action="process_form.py?action=link_scans" method="POST">')
        print(f'<div class="form-group"><label>Scanning Organizer:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{org_options}</select></div>')
        print(f'<div class="form-group"><label>Ticket to Scan:</label><select name="ticket_id" class="form-group" style="width:100%; padding:15px;">{tkt_options}</select></div>')
        print('<button type="submit" class="btn-submit">Scan</button></form>')
    
    else:
        print("<p>Invalid or missing 'form' parameter. Please select a valid option from the maintenance page.</p>")

    print_html_footer()
    
    # Закрываем соединение
    if conn.is_connected():
        cursor.close()
        conn.close()

# Обертка для отлова любых ошибок
try:
    main()
except Exception as e:
    # Если что-то пойдет не так, cgitb должен показать ошибку
    # Но на всякий случай, добавим свой вывод
    print("Content-Type: text/html\n")
    print("<html><body><h1>Critical Script Error</h1>")
    print(f"<p>A critical error occurred that prevented the script from running:</p><pre>{e}</pre>")
    print("</body></html>")