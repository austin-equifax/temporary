import json 
import MySQLdb
from datetime import datetime
import paramiko #2.7.2
from ftplib import FTP 


local_path = "./bi_transfers/"
executed_query_list = []

def populate_db():
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
            with open(local_path + '{query_name}.csv'.format(query_name=query_name),'w') as file:
                for row in results:
                    file.write(str(row) + '\n')

            executed_query_list.append(key)
        print("Queries executed and results saved to text files.")
    
    except MySQLdb.Error as e:
        print(f"Error: {e}")
    
    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()


def transfer_files():
    host = ""
    port = 22 
    username = ""
    password = ""

    remote_path = "workforce/WSAISPROB005/incoming

    ssh_client = paramiko.SSHClient()

    try:
        
        if len(executed_query_list) == 0:
            raise ValueError("No executed queries found")
            
        ssh_client.connect(hostname=host, port=port, username=username, password=password)
        sftp = ssh_client.open_sftp()
    
        # Transfer
        for file_name in executed_query_list:
            local_file = local_path + file_name
            sftp.put(local_file, remote_path)
            print(f"File {local_file} successfully transferred to {remote_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the SFTP session and SSH client
        if 'sftp' in locals():
            sftp.close()
        ssh_client.close()
