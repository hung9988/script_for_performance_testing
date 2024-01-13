import psycopg2
import random
from faker import Faker

# Create a Faker instance
fake = Faker()

# Connect to your database
conn = psycopg2.connect(
    host="localhost",
    database="student_manager",
    user="postgres",
    password="0000"
)

# Create a cursor
cur = conn.cursor()
sql_query=""
# Fetch all enterprise_id values from the enterprises table
cur.execute("SELECT enterprise_id FROM enterprises")
enterprises = [item[0] for item in cur.fetchall()]
cur.execute("SET myapp.user_role='admin';")
# Keep track of the number of scholarships for each enterprise
scholarships_per_enterprise = {enterprise_id: 0 for enterprise_id in enterprises}
scholarship_values = []
sql_query = ""

for _ in range(100):
    while True:
        enterprise_id = fake.random_element(elements=enterprises)
        if scholarships_per_enterprise[enterprise_id] < 4:
            break
    amount = random.randrange(1000000, 10000001, 500000)
    scholarship_description = fake.text(max_nb_chars=200)
    quantity = random.randint(10, 50)

    # Generate the INSERT statement for the current scholarship
    insert_statement = cur.mogrify("""
        INSERT INTO scholarships (enterprise_id, amount, scholarship_description)
        VALUES (%s, %s, %s);
    """, (enterprise_id, amount, scholarship_description)).decode('utf-8')

    # Append the INSERT statement to the sql_query string
    sql_query += insert_statement

    scholarships_per_enterprise[enterprise_id] += 1

# Dump the SQL query into a new file
with open('scholarships.sql', 'w') as f:
    f.write(sql_query)

# Close the cursor and connection
cur.close()
conn.close()