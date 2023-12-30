import boto3
import os
from dotenv import load_dotenv
import logging
from cria_tabela_execucao import criar_tabela_dynamodb_execucao 
from cria_tabela_parametro import  criar_tabela_dynamodb_parametro
from cria_tabela_thread import criar_tabela_dynamodb_thread
load_dotenv('../config/.env')


# Definimos uma função para encapsular nossa pequena aventura no DynamoDB.
def excluir_tabela_dynamodb_teste(table_name='nenhuma'):
  if os.getenv('BANCO')=='LOCAL':
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
  else:
    dynamodb = boto3.resource('dynamodb') 
    
  logging.info('BANCO= '+os.getenv('BANCO'))

  # Nome da tabela que queremos excluir.
  tabela_nome = table_name

  # Pegar a referência da tabela a ser excluída.
  tabela = dynamodb.Table(tabela_nome)

  # Exclui a tabela propriamente.
  tabela.delete()

  # Agora, para a parte mágica da confirmação, vamos esperar a tabela ser eliminada.
  tabela.meta.client.get_waiter('table_not_exists').wait(TableName=tabela_nome)
  print(f"A tabela {tabela_nome} foi eliminada. Acabou-se o que era doce... ou não tão doce.")

# Vamos simular a chamada da função, caso você queira viver aventuras.

try:
  excluir_tabela_dynamodb_teste('poc_azul_cliente')
except Exception as e:
  print(e.response['Error']['Message'])
  logging.error(f"Algo inesperado aconteceu: {e}")
try:
  excluir_tabela_dynamodb_teste('poc_azul_parametro')
except Exception as e:
  print(e.response['Error']['Message'])
  logging.error(f"Algo inesperado aconteceu: {e}")
try:
  excluir_tabela_dynamodb_teste('poc_azul_parametro')
except Exception as e:
  print(e.response['Error']['Message'])
  logging.error(f"Algo inesperado aconteceu: {e}")
  
try:
  excluir_tabela_dynamodb_teste('poc_azul_thread')
except Exception as e:
  print(e.response['Error']['Message'])
  logging.error(f"Algo inesperado aconteceu: {e}")
  
try:
  excluir_tabela_dynamodb_teste('poc_azul_execucao')
except Exception as e:
  print(e.response['Error']['Message'])
  logging.error(f"Algo inesperado aconteceu: {e}")


print("rodou o apaga banco")