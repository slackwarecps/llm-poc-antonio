from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import logging

load_dotenv('../config/.env')

llm = ChatOpenAI()
llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY')) 



llm.invoke("how can langsmith help with testing?")

from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

logging.info("rodou o langchain")
