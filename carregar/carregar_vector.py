from langchain.document_loaders import JSONLoader

import os
from dotenv import load_dotenv
import logging

load_dotenv('../config/.env')
logging.basicConfig(filename='../log/poc-azul.log', encoding='utf-8', level=logging.INFO)

from langchain.text_splitter import TokenTextSplitter

import redis
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Redis

logging.info('OPENAI_API_KEY= ' + os.getenv('OPENAI_API_KEY'))


file_path='../example_data/api-agendamento.json'




loader = JSONLoader(
    file_path='../example_data/api-agendamento.json',
    jq_schema='.messages[].nome',
    text_content=False)

lista_de_agendamentos = loader.load()
#pprint(data)


#CHUNKS
arquivo="/Users/fabioalvaropereira/state_of_the_union.txt"
arquivo2="/Users/fabioalvaropereira/biblia.txt"
with open(arquivo) as f:
    state_of_the_union = f.read()



text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=0, encoding_name='cl100k_base')

texts = text_splitter.split_text(state_of_the_union)
print(texts[0])

# redis
# Precisamos da configuração padrão do nosso pianista Redis
redis_host = "localhost"
redis_port = 6379
redis_password = ""  # Substitua se o seu Redis estiver com senha
# Vamos fazer a conexão com o Redis
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

#os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
logging.info('OPENAI_API_KEY= ' + os.getenv('OPENAI_API_KEY'))
embeddings = OpenAIEmbeddings()

index_schema = {
    "tag": [{"name": "genre"}],
    "text": [{"name": "director"}],
    "numeric": [{"name": "year"}, {"name": "rating"}],
}

docs = [
    Document(
        page_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",
        metadata={
            "year": 1993,
            "rating": 7.7,
            "director": "Steven Spielberg",
            "genre": "science fiction",
        },
    ),
    Document(
        page_content="Leo DiCaprio gets lost in a dream within a dream within a dream within a ...",
        metadata={
            "year": 2010,
            "director": "Christopher Nolan",
            "genre": "science fiction",
            "rating": 8.2,
        },
    ),
    Document(
        page_content="A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea",
        metadata={
            "year": 2006,
            "director": "Satoshi Kon",
            "genre": "science fiction",
            "rating": 8.6,
        },
    ),
    Document(
        page_content="A bunch of normal-sized women are supremely wholesome and some men pine after them",
        metadata={
            "year": 2019,
            "director": "Greta Gerwig",
            "genre": "drama",
            "rating": 8.3,
        },
    ),
    Document(
        page_content="Toys come alive and have a blast doing so",
        metadata={
            "year": 1995,
            "director": "John Lasseter",
            "genre": "animated",
            "rating": 9.1,
        },
    ),
    Document(
        page_content="Three men walk into the Zone, three men walk out of the Zone",
        metadata={
            "year": 1979,
            "rating": 9.9,
            "director": "Andrei Tarkovsky",
            "genre": "science fiction",
        },
    ),
]

vectorstore = Redis.from_documents(
    lista_de_agendamentos,
    embeddings,
    redis_url="redis://localhost:6379",
    index_name="movie_reviews",
    index_schema=index_schema,
)



print("acabou!!! de rodar")