from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from customer_service_bot import CustomerServiceBot
from db_utils import DBConnection
from ticket_system import TicketSystem
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

# Initialize database connection
db_conn = DBConnection()
db_conn.connect()

# Initialize ticket system
ticket_system = TicketSystem()

# Initialize customer service bot
openai_api_key = os.getenv("OPENAI_API_KEY")
customer_service_bot = CustomerServiceBot(db_conn, openai_api_key)

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(chat_input: ChatInput):
    try:
        response = customer_service_bot.chat(chat_input.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_ticket")
async def create_ticket(chat_input: ChatInput):
    try:
        ticket_id = ticket_system.create_ticket(chat_input.message)
        return {"ticket_id": ticket_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ticket/{ticket_id}")
async def get_ticket(ticket_id: str):
    ticket = ticket_system.get_ticket(ticket_id)
    if ticket:
        return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.on_event("startup")
async def startup_event():
    # Initialize database and update knowledge base
    db_conn.connect()
    db_conn.execute("SELECT 1")  # Test connection
    print("Database connected successfully")

@app.on_event("shutdown")
async def shutdown_event():
    db_conn.disconnect()
    print("Database connection closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)