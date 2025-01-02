# ALL EXTERNAL LIBRARIES ARE IN HERE
# MAKES SURE ALL DEPENDENCIES ARE MET!

import customtkinter
import socket
import socketserver
import random
import threading
from colorama import Fore, init
import psycopg2
import wsgiref.simple_server
from psycopg2.extras import RealDictCursor
import json

# Database Connection

def db_connection():
    try:
        connection = psycopg2.connect(
            database="LAN-CHAT-APP",
            user="postgres",
            password="Pangbourne4!",
            host="localhost",
            port="5432"
        )
        print("DB connect successful.")
        return connection
    except Exception as e:
        print("Error connect unsuccessful.", e)
        return None

# Connection Test

if __name__ == "__main__":
    conn = db_connection()
    if conn:
        print("Connection is working")
        conn.close()
    else:
        print("Connection failed")
