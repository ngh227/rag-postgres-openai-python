import openai
from db_utils import get_relevant_info
from ticket_system import create_ticket
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class CustomerServiceBot:
    def __init__(self, db_conn, openai_api_key):
        self.db_conn = db_conn
        openai.api_key = openai_api_key

    def get_response(self, user_input):
        relevant_info = get_relevant_info(self.db_conn, user_input)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful customer service assistant for Peacock Hill Productions. Use the following information to answer questions: " + relevant_info},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response.choices[0].message['content']
            
            if "I'm sorry, I don't have enough information" in ai_response or "I can't assist with that" in ai_response:
                # Use your existing ticket creation logic here
                return "I'm sorry, I couldn't fully answer your question. I'll create a ticket for further assistance."
            else:
                return ai_response
        except Exception as e:
            # Use your existing error handling logic here
            return f"I apologize, but I encountered an error: {str(e)}"

    def chat(self, user_input):
        # First, try to answer the question using GPT
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful customer service assistant."},
                {"role": "user", "content": user_input},
            ],
        )

        ai_response = response.choices[0].message.content

        # Check if the AI could answer confidently
        if "I'm not sure" in ai_response or "I don't have enough information" in ai_response:
            # If not, create a ticket
            ticket_id = create_ticket(user_input)
            return f"I'm sorry, but I couldn't fully answer your question. I've created a ticket (ID: {ticket_id}) for our human staff to assist you further."
        else:
            return ai_response

    def run(self):
        print("Welcome to Customer Service. How can I help you today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Thank you for using our service. Goodbye!")
                break
            response = self.chat(user_input)
            print("Bot:", response)


if __name__ == "__main__":
    bot = CustomerServiceBot()
    bot.run()
