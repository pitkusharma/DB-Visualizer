from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
import os


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)
