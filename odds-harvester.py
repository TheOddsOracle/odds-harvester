import requests
import json
import pymysql

base_url = 'https://api.the-odds-api.com'
api_key = '03b0ed79afb3e22a0458b0f9cb51bfc3'
api_version = 'v4'

 Get Sports

def fetch_and_store_sports(api_url, db_config):
    # Make the HTTP request
    response = requests.get(api_url)
    if response.status_code != 200:
        print("Failed to fetch data")
        return

    # Parse JSON response
    sports_data = response.json()

    # Connect to the MySQL database
    connection = pymysql.connect(host=db_config['host'],
                                 user=db_config['user'],
                                 password=db_config['password'],
                                 db=db_config['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # SQL statement for inserting data
            sql = "INSERT INTO sports (sport_key, sport_group, title, description, active, has_outrights) VALUES (%s, %s, %s, %s, %s, %s)"

            # Insert each sport into the database
            for sport in sports_data:
                cursor.execute(sql, (sport['key'], sport['group'], sport['title'], sport['description'], sport['active'], sport['has_outrights']))

        # Commit the changes
        connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        connection.close()

    print("Data inserted successfully into the sports table.")

api_url = f"https://api.the-odds-api.com/v4/sports/?apiKey={api_key}"
db_config = {
    'host': 'localhost',
    'user': '',
    'password': '',
    'db': 'odds'
}

fetch_and_store_sports(api_url, db_config)

