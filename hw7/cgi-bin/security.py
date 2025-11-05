#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import hashlib
import mysql.connector

db_config = { 'host': 'localhost', 'database': 'db_kjurabaev', 'user': 'kjurabaev', 'password': '5tr8zjbrDq1GchfY' }

def check_credentials(form):
    username = form.getvalue('admin_user')
    password = form.getvalue('admin_pass')

    if not (username and password):
        return False

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password_hash FROM AdminUsers WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        
        if user_data and user_data['password_hash'] == password_hash:
            return True
        else:
            return False
    except:
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()