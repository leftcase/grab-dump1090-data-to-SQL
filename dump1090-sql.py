import socket
import sqlite3

# Probably only use this for a short period of time, and only if you're curious about
# the data coming from your dump1090 install. It hammers your disk, and creates 
# a massive SQLite database quite quickly. If you're running this on a Pi, it 
# will destroy your SD card quickly.

# Create your SQLite database here
sqlite_database = r"C:\Users\chris\Music\NoOneDriveSync\flight_database.db"

def get_1090(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    while True:
        data = s.recv(1024)
        if not data:
            break
        # Break received data down into lists for processing by SQLite
        msg = data.decode('utf-8')
        submsg = msg.splitlines()
        for e in submsg: 
            data_list = e.split(',')
            database(data_list)
    s.close()

def database(msg):
    conn = sqlite3.connect(sqlite_database)
    c = conn.cursor()
    insert_statement = ('''
        INSERT INTO data 
        (message_type, 
        transmission_type,
        session_id,
        aircraft_id,
        hexident,
        flight_id,
        date_msg_generated,
        time_msg_generated,
        date_msg_logged,
        time_msg_logged,
        callsign,
        altitude,
        ground_speed,
        track,
        lat,
        long,
        vertical_rate,
        squawk,
        alert_squawk_change,
        emergency,
        spi,
        is_on_ground)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    ''')
    print(msg)
    # Sometimes a list is shorter than the 22 items expected. I don't know why, and as messages are repeated I'm 
    # not going to invest too much time in figuring it out. This is a kludge to get around it.
    if len(msg) == 22:
        c.execute(insert_statement,msg)
        conn.commit()
    else:
        pass

# Create the database if it hasn't been created already
conn = sqlite3.connect(sqlite_database)
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS data
          (msg_id INTEGER PRIMARY KEY,
          message_type varchar(20),
          transmission_type varchar(20),
          session_id varchar(20),
          aircraft_id varchar(20),
          hexident varchar(20),
          flight_id varchar(20),
          date_msg_generated varchar(20),
          time_msg_generated varchar(20),
          date_msg_logged varchar(20),
          time_msg_logged varchar(20),
          callsign varchar(20),
          altitude int,
          ground_speed int,
          track int,
          lat float,
          long float,
          vertical_rate int,
          squawk int,
          alert_squawk_change int,
          emergency int,
          spi varchar(20),
          is_on_ground varchar(20))
          ''')
conn.commit()

# Enter your dump1090 IP here
get_1090('192.168.1.138','30003')
