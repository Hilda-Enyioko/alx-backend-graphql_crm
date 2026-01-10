from django_crontab import crontab
from datetime import datetime
import logging
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

logging.basicConfig(level=logging.INFO)

def log_crm_heartbeat():
    # Log heartbeat every 5 mins
    message = f"{datetime.now().strftime("DD/MM/YYYY-HH:MM:SS")} CRM is alive"
    
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message)
        
    logging.info(message.strip())
    
    
    # Use gql to query the hello field
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("{ hello }")
        result = client.execute(query)
        
        if "hello" in result:
            logging.info("GraphQL endpoint responsive")
        else:
            logging.warning("GraphQL endpoint did not return 'hello'")
    except Exception as e:
        logging.error(f"Error contacting GraphQL endpoint: {e}")


if __name__ == "__main__":
    log_crm_heartbeat()