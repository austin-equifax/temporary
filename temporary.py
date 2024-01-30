import json 
import MySQLdb
from datetime import datetime
from ftplib import FTP 

db_host = ""
db_username = ""
db_password = ""
db_name = ""

try:
    conn = MySQLdb.connect(host=db_host, user=db_username, passwd=db_password, db=db_name)

    # Create a cursor object
    cursor = conn.cursor()

    # Define two SQL queries to execute
    query_dict = {
        license_source: ""
        
        sanctions_source: ""
        sanctions_products: ""
        sanctions_tags: ""
    
        healthstats_data: ""
        healthstats_products: ""
        healthstats_tags: ""
    }

for key, val in query_dict.items():
    # Execute the first SQL query
    cursor.execute(val)
    results = cursor.fetchall()

    date_object = datetime.now(tz=timezone.utc)
    date_string = "_" + date_object.strftime('%Y%m%d_%H:%M:%S')
    query_name = key + date_string

    # Output results of the first query to a text file
    with open('{query_name}.csv'.format(query_name=query_name),'w') as file:
        for row in results:
            file.write(str(row) + '\n')

print("Queries executed and results saved to text files.")

except MySQLdb.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and the connection
    cursor.close()
    conn.close()

ftp_server = ""
email = ""
username = ""
password = ""

def lambda_handler(event, context):
    status = None 
    try:
        ftp = FTP(ftp_server)
        ftp.login(user=username, passwd=password)
        with open("source.txt", "rb") as source_file:
            ftp.storbinary("STOR source.txt", source_file)

        status = "passed"
    except Exception as e:
        status = e
    
    return {
        'statusCode': 200,
        'body': json.dumps(status)
    }
