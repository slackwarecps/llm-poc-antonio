import boto3
import os
from dotenv import load_dotenv
import logging

load_dotenv('../config/.env')

import boto3

# Iniciamos pela definição da nossa função elegante para criar a tabela.
def criar_tabela_dynamodb_parametro(dynamodb=None):
    # Primeiro convocamos um cliente para o recurso DynamoDB.
    if os.getenv('BANCO')=='LOCAL':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    else:
        dynamodb = boto3.resource('dynamodb') 

    # Explicamos com elegância o nosso plano para a tabela.
    tabela_nome = 'poc_azul_parametro'
    chave_particao_nome = 'id'
    chave_particao_tipo = 'N'  # 'S' para String

    # Invocamos o método de criação da tabela com todos os parametros necessários.
    tabela = dynamodb.create_table(
        TableName=tabela_nome,
        KeySchema=[
            {
                'AttributeName': chave_particao_nome,
                'KeyType': 'HASH'  # HASH refere-se à chave de partição
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': chave_particao_nome,
                'AttributeType': chave_particao_tipo
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Calma, é preciso esperar... a tabela está sendo montada.
    tabela.meta.client.get_waiter('table_exists').wait(TableName=tabela_nome)
    print(f"A belíssima tabela {tabela_nome} está pronta para o baile!")

# Convocamos a função para a ação apenas se estiveres pronto para a festa.
# criar_tabela_telefone_dynamodb()