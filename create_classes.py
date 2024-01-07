from datetime import datetime, time, timedelta
from faker import Faker
import psycopg2
import random

fake = Faker()

# Connect to your postgres DB
conn = psycopg2.connect("dbname=hust_student_manager user=postgres password=0000 host=localhost")

# Open a cursor to perform database operations
cur = conn.cursor()

# Fetch all teacher_id and school_id values from the teachers table
cur.execute("SELECT teacher_id, school_id FROM teachers")
teachers = {}
for row in cur.fetchall():
    teacher_id, school_id = row
    if school_id not in teachers:
        teachers[school_id] = []
    teachers[school_id].append(teacher_id)

# Fetch all subject_id and school_id values from the subjects table
cur.execute("SELECT subject_id, school_id FROM subjects")
subjects = {}
for row in cur.fetchall():
    subject_id, school_id = row
    if school_id not in subjects:
        subjects[school_id] = []
    subjects[school_id].append(subject_id)

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
locations = [f'{chr(65 + i)}{j}' for i in range(5) for j in range(10)]
used_locations = {}

# Generate 1000 random add_class function calls
with open('select_commands.sql', 'w') as f:
    # Generate 1000 random add_class function calls
    for _ in range(1000):
        school_id = random.choice(list(teachers.keys()))
        teacher_id = random.choice(teachers[school_id])
        subject_id = random.choice(subjects[school_id])
        capacity = random.randint(10, 50)
        day_of_week = random.choice(days_of_week)
        location = random.choice(locations)
        start_time = (datetime.now() + timedelta(minutes=random.randint(1, 60))).time()
        end_time = (datetime.now() + timedelta(minutes=random.randint(61, 120))).time()

        # Write the command to the file
        f.write(f"""
            SELECT * FROM add_class({teacher_id}, '{subject_id}', {capacity}, '{day_of_week}', '{location}', '{start_time}'::time, '{end_time}'::time);
        """)
# Close communication with the database
conn.commit()
cur.close()
conn.close()