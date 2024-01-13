from faker import Faker
import psycopg2
import random
from datetime import datetime, time, timedelta

# ...
fake = Faker()

# Connect to your postgres DB
conn = psycopg2.connect("dbname=student_manager user=postgres password=0000 host=localhost")

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
start_times = [time(hour=6, minute=45, second=0)]
start_times2 = [time(hour=6, minute=45, second=0).strftime('%H:%M:%S')]
while start_times[-1] < time(hour=16, minute=45, second=0):
    start_datetime = datetime.combine(datetime.today(), start_times[-1])
    next_start_datetime = start_datetime + timedelta(minutes=45)
    start_times.append(next_start_datetime.time())
    start_times2.append(next_start_datetime.time().strftime('%H:%M:%S'))

i=1
for class_id in range(1, 301):
    i+=1
    print(i)
    school_id = fake.random_element(elements=list(teachers.keys()))
    teacher_id = fake.random_element(elements=teachers[school_id])
    subject_id = fake.random_element(elements=subjects[school_id])
    external_resources = fake.url()
    capacity = fake.random_int(min=40, max=100)
    day_of_week = fake.random_element(elements=days_of_week)
    location = fake.random_element(elements=locations)
    i+=1
    print(i)
    print(day_of_week)
    print(location)
    print
    while (day_of_week, location) in used_locations:
        day_of_week = fake.random_element(elements=days_of_week)
        location = fake.random_element(elements=locations)
    temp = fake.random_element(elements=start_times2)
    start_time = datetime.strptime(temp, '%H:%M:%S').time()
    start_datetime = datetime.combine(datetime.today(), start_time)
    duration = timedelta(hours=1 if start_time.minute == 0 else 3, minutes=30 if start_time.minute == 0 else 0)
    end_datetime = start_datetime + duration
    end_time = end_datetime.time()
    used_locations[(day_of_week, location)] = (start_time, end_time)
    cur.execute("""
        INSERT INTO classes (class_id, teacher_id, subject_id, capacity,day_of_week, location, start_time, end_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (class_id, teacher_id, subject_id, capacity,day_of_week, location, start_time.strftime('%H:%M:%S'), end_time.strftime('%H:%M:%S')))
  

# Close communication with the database
conn.commit()
cur.close()
conn.close()