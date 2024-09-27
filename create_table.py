import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(user='root', password='Aarya@1971', host='localhost', database='mfdb')

# Create a cursor object
cursor = cnx.cursor()

# Create the table
query = """
CREATE TABLE mutual_funds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    category_rank VARCHAR(255),
    morningstar_rating VARCHAR(255),
    nav VARCHAR(255),
    fund_return VARCHAR(255),
    category_return VARCHAR(255),
    risk VARCHAR(255),
    fund_size VARCHAR(255)
)
"""
cursor.execute(query)

# Close the cursor and connection
cursor.close()
cnx.close()