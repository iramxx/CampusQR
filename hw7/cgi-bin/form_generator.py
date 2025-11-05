#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

import cgi
import mysql.connector
import os
import security

username = os.environ.get('USER', 'kjurabaev')

def print_html_header(title):
    print("Content-Type: text/html\n")
    print(f"<html><head><title>{title}</title><link rel='stylesheet' href='/~{username}/auth-style.css'></head><body>")
    print(f"<div class='auth-container'><div class='form-container'><h2>{title}</h2>")

def print_html_footer(back_link=True):
    if back_link:
        print(f"<a href='javascript:history.back()' class='back-link'>← Back</a>")
    print("</div></div></body></html>")

def get_select_options(cursor, query):
    cursor.execute(query)
    items = cursor.fetchall()
    options = ""
    for item in items:
        options += f"<option value='{item[0]}'>{item[1]}</option>\n"
    return options

def print_hidden_fields(form):
    print(f"<input type='hidden' name='admin_user' value='{form.getvalue('admin_user')}'>")
    print(f"<input type='hidden' name='admin_pass' value='{form.getvalue('admin_pass')}'>")

def main():
    form = cgi.FieldStorage()
    
    if not security.check_credentials(form):
        print_html_header("Access Denied")
        print("<p style='color: red;'>Invalid username or password.</p>")
        print(f"<a href='/~{username}/maintenance.html' class='back-link'>← Try Again</a></div></div></body></html>")
        return

    conn = mysql.connector.connect(**security.db_config)
    cursor = conn.cursor()
    
    form_type = form.getvalue('form')
    
    if form_type == 'maintenance_hub':
        print_html_header("Data Maintenance")
        print("""
            <div style="text-align: left;">
                <h3>Step 1: Create Base Objects</h3>
                <ul>
                    <li><a href="form_generator.py?form=add_user&admin_user={user}&admin_pass={password}">1. Add User</a></li>
                    <li><a href="form_generator.py?form=add_talk&admin_user={user}&admin_pass={password}">2. Add Talk Event</a></li>
                    <li><a href="form_generator.py?form=add_workshop&admin_user={user}&admin_pass={password}">3. Add Workshop Event</a></li>
                    <li><a href="form_generator.py?form=add_organizer&admin_user={user}&admin_pass={password}">4. Create Organizer Profile</a></li>
                    <li><a href="form_generator.py?form=add_attendee&admin_user={user}&admin_pass={password}">5. Create Attendee Profile</a></li>
                    <li><a href="form_generator.py?form=add_ticket&admin_user={user}&admin_pass={password}">6. Create Student/Guest Ticket</a></li>
                </ul>
                <h3>Step 2: Create Links</h3>
                <ul>
                    <li><a href="form_generator.py?form=link_creates&admin_user={user}&admin_pass={password}">1. Link Organizer to Event (Creates)</a></li>
                    <li><a href="form_generator.py?form=link_register_to&admin_user={user}&admin_pass={password}">2. Register Attendee for Event (Register_to)</a></li>
                    <li><a href="form_generator.py?form=link_scans&admin_user={user}&admin_pass={password}">3. Scan a Ticket</a></li>
                </ul>
            </div>
        """.format(user=form.getvalue('admin_user'), password=form.getvalue('admin_pass')))
        print_html_footer(False)

    elif form_type == 'add_user':
        print_html_header("Add New User")
        print('<form action="process_form.py?action=add_user" method="POST">')
        print_hidden_fields(form)
        print('<div class="form-group"><input type="text" name="name" required placeholder="User Name"></div>')
        print('<div class="form-group"><input type="email" name="email" required placeholder="User Email"></div>')
        print('<div class="form-group"><input type="password" name="password" required placeholder="Password"></div>')
        print('<button type="submit" class="btn-submit">Add User</button></form>')
        print_html_footer()

    elif form_type == 'add_talk':
        print_html_header("Add New Talk Event")
        print('<form action="process_form.py?action=add_talk" method="POST">')
        print_hidden_fields(form)
        print('<div class="form-group"><input type="text" name="title" required placeholder="Talk Title"></div>')
        print('<div class="form-group"><input type="text" name="speaker_name" required placeholder="Speaker\'s Name"></div>')
        print('<div class="form-group"><label>Date and Time</label><input type="datetime-local" name="event_date" required></div>')
        print('<div class="form-group"><textarea name="description" required placeholder="Description"></textarea></div>')
        print('<div class="form-group"><input type="number" name="capacity" required placeholder="Capacity"></div>')
        print('<button type="submit" class="btn-submit">Add Talk</button></form>')
        print_html_footer()

    elif form_type == 'add_workshop':
        print_html_header("Add New Workshop Event")
        print('<form action="process_form.py?action=add_workshop" method="POST">')
        print_hidden_fields(form)
        print('<div class="form-group"><input type="text" name="title" required placeholder="Workshop Title"></div>')
        print('<div class="form-group"><label>Date and Time</label><input type="datetime-local" name="event_date" required></div>')
        print('<div class="form-group"><textarea name="description" required placeholder="Description"></textarea></div>')
        print('<div class="form-group"><input type="number" name="capacity" required placeholder="Capacity"></div>')
        print('<div class="form-group"><input type="text" name="event_type" value="Workshop" readonly style="background-color: #f0f0f0;"></div>')
        print('<button type="submit" class="btn-submit">Add Workshop</button></form>')
        print_html_footer()

    elif form_type == 'add_organizer':
        options = get_select_options(cursor, "SELECT user_id, name FROM Users WHERE user_id NOT IN (SELECT user_id FROM Organizers)")
        print_html_header("Create Organizer Profile")
        print('<form action="process_form.py?action=add_organizer" method="POST">')
        print_hidden_fields(form)
        print(f'<div class="form-group"><label>Select User:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<div class="form-group"><input type="text" name="club_name" required placeholder="Club Name"></div>')
        print('<button type="submit" class="btn-submit">Create Profile</button></form>')
        print_html_footer()

    elif form_type == 'add_attendee':
        options = get_select_options(cursor, "SELECT user_id, name FROM Users WHERE user_id NOT IN (SELECT user_id FROM Attendee)")
        print_html_header("Create Attendee Profile")
        print('<form action="process_form.py?action=add_attendee" method="POST">')
        print_hidden_fields(form)
        print(f'<div class="form-group"><label>Select User:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<div class="form-group"><input type="text" name="student_id" required placeholder="Student ID"></div>')
        print('<button type="submit" class="btn-submit">Create Profile</button></form>')
        print_html_footer()

    elif form_type == 'add_ticket':
        options = get_select_options(cursor, "SELECT user_id, name FROM Users")
        print_html_header("Create Student/Guest Ticket")
        print('<form action="process_form.py?action=add_ticket" method="POST">')
        print_hidden_fields(form)
        print(f'<div class="form-group"><label>Assign ticket to User:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<button type="submit" class="btn-submit">Create Ticket</button></form>')
        print_html_footer()
    
    elif form_type == 'link_creates':
        org_options = get_select_options(cursor, "SELECT U.user_id, U.name FROM Users U JOIN Organizers O ON U.user_id = O.user_id")
        evt_options = get_select_options(cursor, "SELECT event_id, title FROM Events")
        print_html_header("Link Organizer to Event")
        print('<form action="process_form.py?action=link_creates" method="POST">')
        print_hidden_fields(form)
        print(f'<div class="form-group"><label>Organizer:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{org_options}</select></div>')
        print(f'<div class="form-group"><label>Event:</label><select name="event_id" class="form-group" style="width:100%; padding:15px;">{evt_options}</select></div>')
        print('<button type="submit" class="btn-submit">Link</button></form>')
        print_html_footer()

    elif form_type == 'link_register_to':
        att_options = get_select_options(cursor, "SELECT U.user_id, U.name FROM Users U JOIN Attendee A ON U.user_id = A.user_id")
        evt_options = get_select_options(cursor, "SELECT event_id, title FROM Events")
        print_html_header("Register Attendee for Event")
        print('<form action="process_form.py?action=link_register_to" method="POST">')
        print_hidden_fields(form)
        print(f'<div class="form-group"><label>Attendee:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{att_options}</select></div>')
        print(f'<div class="form-group"><label>Event:</label><select name="event_id" class="form-group" style="width:100%; padding:15px;">{evt_options}</select></div>')
        print('<button type="submit" class="btn-submit">Register</button></form>')
        print_html_footer()

    elif form_type == 'link_scans':
        org_options = get_select_options(cursor, "SELECT U.user_id, U.name FROM Users U JOIN Organizers O ON U.user_id = O.user_id")
        tkt_options = get_select_options(cursor, "SELECT ticket_id, qr_code_data FROM Tickets WHERE status = 'issued'")
        print_html_header("Scan a Ticket")
        print('<form action="process_form.py?action=link_scans" method="POST">')
        print_hidden_fields(form)
        print(f'<div class="form-group"><label>Scanning Organizer:</label><select name="user_id" class="form-group" style="width:100%; padding:15px;">{org_options}</select></div>')
        print(f'<div class="form-group"><label>Ticket to Scan:</label><select name="ticket_id" class="form-group" style="width:100%; padding:15px;">{tkt_options}</select></div>')
        print('<button type="submit" class="btn-submit">Scan</button></form>')
        print_html_footer()
    
    else:
        print_html_header("Error")
        print("<p>Invalid or missing 'form' parameter. Please select a valid option from the maintenance page.</p>")
        print_html_footer()

    if conn.is_connected():
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()