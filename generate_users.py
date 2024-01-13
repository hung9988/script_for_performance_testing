from faker import Faker
import psycopg2

fake = Faker()

user_id = 20220000

def create_fake_user(role):
    global user_id
    user = {
        'user_id': user_id,
        'email': fake.unique.email(),
        'hashed_password': fake.password(length=10),
        'role': role,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'dob': None if role == 'enterprises' else fake.date_of_birth(minimum_age=22, maximum_age=60)
    }
    user_id += 1
    return user

def create_fake_teacher(user_id):
    return {
        'teacher_id': user_id,
        'school_id': fake.random_int(min=1, max=6),
        'hired_year': fake.random_int(min=2012, max=2022),
        'qualification': fake.job()
    }

def create_fake_student(user_id):
    return {
        'student_id': user_id,
        'program_id': fake.random_int(min=1, max=100),
        'enrolled_year': fake.random_int(min=2018, max=2023)
    }

def create_fake_enterprise(user_id):
    return {
        'enterprise_id': user_id,
        'enterprise_name': fake.unique.company(),
        'contact': fake.phone_number()
    }

# Connect to your postgres DB
# Connect to your postgres DB
conn = psycopg2.connect("dbname=student_manager user=postgres password=0000 host=localhost")

# Open a cursor to perform database operations
cur = conn.cursor()

# Number of each user type to create
num_teachers = 500
num_enterprises = 500
num_students = 9000

# Create teachers
for _ in range(num_teachers):
    user = create_fake_user('teacher')
    cur.execute("""
        INSERT INTO users (user_id, email, password, role, first_name, last_name, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user['user_id'], user['email'], user['hashed_password'], user['role'], user['first_name'], user['last_name'], user['dob']))
    teacher = create_fake_teacher(user['user_id'])
    cur.execute("""
        INSERT INTO teachers (teacher_id, school_id, hired_year, qualification)
        VALUES (%s, %s, %s, %s)
    """, (teacher['teacher_id'], teacher['school_id'], teacher['hired_year'], teacher['qualification']))

# Create enterprises
for _ in range(num_enterprises):
    user = create_fake_user('enterprise')
    cur.execute("""
        INSERT INTO users (user_id, email, password, role )
        VALUES (%s, %s, %s, %s)
    """, (user['user_id'], user['email'], user['hashed_password'], user['role']))
    enterprise = create_fake_enterprise(user['user_id'])
    cur.execute("""
        INSERT INTO enterprises (enterprise_id, enterprise_name, contact)
        VALUES (%s, %s, %s)
    """, (enterprise['enterprise_id'], enterprise['enterprise_name'], enterprise['contact']))

# Create students
for _ in range(num_students):
    user = create_fake_user('student')
    cur.execute("""
        INSERT INTO users (user_id, email, password, role, first_name, last_name, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user['user_id'], user['email'], user['hashed_password'], user['role'], user['first_name'], user['last_name'], user['dob']))
    student = create_fake_student(user['user_id'])
    cur.execute("""
        INSERT INTO students (student_id, program_id, enrolled_year)
        VALUES (%s, %s, %s)
    """, (student['student_id'], student['program_id'], student['enrolled_year']))

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()