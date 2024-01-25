import json 
from ftplib import FTP 

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
