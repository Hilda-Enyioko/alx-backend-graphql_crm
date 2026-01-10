#!/usr/bin/env python
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE="/tmp/order_reminders_log.txt"

def main():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    
    client = Client(transport=transport, 
                    fetch_schema_from_transport=True)
    
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
    
    query = gql(
        """
        query GetRecentPendingOrders($date: DateTime!) {
            orders(order_date_Gte: $date, status:"Pending") {
                id
                customer {
                    email
                }
            }
        }
        """
    )
    
    result = client.execute(query, variable_values={"date":seven_days_ago})
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(LOG_FILE, "a") as log:
        for order in result.get("orders",[]):
            log.write(
                f"{timestamp} - Order ID: {order['id']}, "
                f"Customer Email:{order['customer']['email']}\n"
            )
            
    print("Order reminders processed!")
    
if __name__=="main":
    main()