from django_crontab import crontab
from datetime import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO)

def log_crm_heartbeat():
    # Log heartbeat every 5 mins
    message = f"{datetime.now().strftime("DD/MM/YYYY-HH:MM:SS")} CRM is alive"
    
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message)
        
    logging.info(message.strip())
    
    # Check GraphQL endpoint
    try:
        graphql_url = "http://localhost:8000/graphql"
        query ='{hello}'
        
        response = requests.post(graphql_url, 
                                 json={'query': query},
                                 timeout=5)
        
        if response.status_code == 200:
            logging.info("GraphQL endpoint responsive")
        else:
            logging.warning(f"GraphQL endpoint returned status {response.status_code}")
            
    except Exception as e:
        logging.error(f"Error contacting GraphQL endpoint: {e}")