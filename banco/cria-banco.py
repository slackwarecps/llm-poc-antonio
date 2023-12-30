import boto3
import os
from dotenv import load_dotenv
import logging
from cria_tabela_cliente import criar_tabela_dynamodb_cliente
from cria_tabela_execucao import criar_tabela_dynamodb_execucao 
from cria_tabela_parametro import  criar_tabela_dynamodb_parametro
from cria_tabela_thread import criar_tabela_dynamodb_thread
load_dotenv('../config/.env')

# Bora ver a mágica acontecer?
criar_tabela_dynamodb_cliente()
criar_tabela_dynamodb_execucao()
criar_tabela_dynamodb_parametro()
criar_tabela_dynamodb_thread()
print("rodou")