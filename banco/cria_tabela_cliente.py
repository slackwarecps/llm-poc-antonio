import boto3
import os
from dotenv import load_dotenv
import logging

load_dotenv('../config/.env')

import boto3
# Vamos fingir que estamos criando este código juntos como uma turma de tecnologia
def criar_tabela_dynamodb_cliente(dynamodb=None):
  if os.getenv('BANCO')=='LOCAL':
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
  else:
    dynamodb = boto3.resource('dynamodb') 
  tabela_nome = 'poc_azul_cliente'
  chave_particao_nome = 'telefone'
  chave_particao_tipo = 'S'  
  # Criar a tabela
  tabela = dynamodb.create_table(
      TableName=tabela_nome,
      KeySchema=[
          {
              'AttributeName': chave_particao_nome,
              'KeyType': 'HASH'  # HASH é a chave de partição
          },
      ],
      AttributeDefinitions=[
          {
              'AttributeName': chave_particao_nome,
              'AttributeType': chave_particao_tipo
          },
      ],
      ProvisionedThroughput={
          'ReadCapacityUnits': 1,
          'WriteCapacityUnits': 1
      }
  )
  # Esperar a tabela ser criada
  tabela.meta.client.get_waiter('table_exists').wait(TableName=tabela_nome)
  print(f"A tabela {tabela_nome} foi criada com sucesso!")