import uuid
from datetime import datetime

from db_utils import DBConnection


class TicketSystem:
    def __init__(self):
        self.db = DBConnection()

    def create_ticket(self, user_query):
        ticket_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        status = "Open"

        # Insert the ticket into the database
        query = """
        INSERT INTO tickets (id, timestamp, query, status)
        VALUES (%s, %s, %s, %s)
        """
        self.db.execute(query, (ticket_id, timestamp, user_query, status))

        return ticket_id

    def get_ticket(self, ticket_id):
        query = "SELECT * FROM tickets WHERE id = %s"
        result = self.db.fetch_one(query, (ticket_id,))
        return result

    def update_ticket_status(self, ticket_id, new_status):
        query = "UPDATE tickets SET status = %s WHERE id = %s"
        self.db.execute(query, (new_status, ticket_id))

    def get_open_tickets(self):
        query = "SELECT * FROM tickets WHERE status = 'Open'"
        return self.db.fetch_all(query)


# Global instance of TicketSystem
ticket_system = TicketSystem()


def create_ticket(user_query):
    """
    Create a new ticket and return the ticket ID.
    This function can be imported and used by other modules.
    """
    return ticket_system.create_ticket(user_query)
