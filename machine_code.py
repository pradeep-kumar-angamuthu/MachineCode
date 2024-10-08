import random
import time
import sqlite3
import os

# Function to generate random values based on the given field's constraints
def generate_tool_offset():
    return round(random.uniform(5, 40), 2)

def generate_feedrate():
    return random.randint(0, 20000)

def generate_tool_in_use(tool_capacity):
    return random.randint(1, tool_capacity)

# Connect to the SQLite database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'machine_data.db')
print(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables (machines, axes, and machine_data)
cursor.execute('''CREATE TABLE IF NOT EXISTS machines (
                    machine_id INTEGER PRIMARY KEY, 
                    machine_name TEXT, 
                    tool_capacity INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS axes (
                    axis_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    axis_name TEXT UNIQUE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS machine_data (
                    machine_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    machine_id INTEGER, 
                    axis_id INTEGER, 
                    tool_offset REAL, 
                    feedrate INTEGER, 
                    tool_in_use INTEGER NULL, 
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

# Define 20 machines with unique machine_ids and tool_capacity
machines = [(81258856 + i, f'EMXP{i+1}', 24) for i in range(20)]
axes = ['X', 'Y', 'Z', 'A', 'C']

# Insert machine and axis data (ensure axis uniqueness)
cursor.executemany('INSERT OR IGNORE INTO machines (machine_id, machine_name, tool_capacity) VALUES (?, ?, ?)', machines)
cursor.executemany('INSERT OR IGNORE INTO axes (axis_name) VALUES (?)', [(axis,) for axis in axes])
print("machine and axes values stored")
conn.commit()

# Set update intervals
tool_update_interval = 300  # 5 minutes for tool_in_use
general_update_interval = 900  # 15 minutes for other fields 900

# Keep track of time
last_general_update = time.time()
last_tool_update = time.time()

# Data generation loop
while True:
    current_time = time.time()

    # Update general fields (tool_offset and feedrate) every 15 minutes
    if current_time - last_general_update >= general_update_interval:
        for machine in machines:
            for axis in axes:
                tool_offset = generate_tool_offset()
                feedrate = generate_feedrate()

                cursor.execute('''INSERT INTO machine_data (machine_id, axis_id, tool_offset, feedrate, tool_in_use, timestamp) 
                                  VALUES (?, (SELECT axis_id FROM axes WHERE axis_name = ?), ?, ?, ?, datetime('now'))''', 
                               (machine[0], axis, tool_offset, feedrate,0))
                print("machine data inserted")

        conn.commit()
        last_general_update = current_time

    # Update tool_in_use every 5 minutes
    if current_time - last_tool_update >= tool_update_interval:
        for machine in machines:
            for axis in axes:
                tool_in_use = generate_tool_in_use(machine[2])

                # Fetch the latest machine_data_id for the specific machine and axis
                cursor.execute('''SELECT machine_data_id 
                                  FROM machine_data 
                                  WHERE machine_id = ? 
                                  AND axis_id = (SELECT axis_id FROM axes WHERE axis_name = ?)
                                  ORDER BY timestamp DESC 
                                  LIMIT 1''', (machine[0], axis))

                latest_record = cursor.fetchone()
                
                if latest_record:  # Check if a record exists
                    # Now update the tool_in_use for the latest record
                    cursor.execute('''UPDATE machine_data 
                                      SET tool_in_use = ? 
                                      WHERE machine_data_id = ?''', 
                                   (tool_in_use, latest_record[0]))
                    print("update machine data inserted")

        conn.commit()
        last_tool_update = current_time

    # Sleep for a short interval to avoid busy-waiting
    time.sleep(60)  # Check every minute

# Close the database connection
conn.close()
