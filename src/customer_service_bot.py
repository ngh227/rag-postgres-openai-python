import openai
from db_utils import DBConnection

from ticket_system import create_ticket


class CustomerServiceBot:
    def __init__(self):
        self.db = DBConnection()
        self.openai = openai.OpenAI()  # Initialize with your API key

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
