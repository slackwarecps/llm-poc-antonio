import boto3
import os
from dotenv import load_dotenv
import logging

load_dotenv('../config/.env')

import boto3

# Iniciamos pela definição da nossa função elegante para criar a tabela.
def criar_tabela_dynamodb_thread(dynamodb=None):
    # Primeiro convocamos um cliente para o recurso DynamoDB.
    if os.getenv('BANCO')=='LOCAL':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    else:
        dynamodb = boto3.resource('dynamodb') 

    # Explicamos com elegância o nosso plano para a tabela.
    tabela_nome = 'poc_azul_thread'
    chave_particao_nome = 'telefone'
    chave_particao_tipo = 'S'  # 'S' para String
    chave_ordenacao_nome = 'status'
    chave_ordenacao_tipo = 'S'  # 'N' para Número (inteiro)

    # Invocamos o método de criação da tabela com todos os parametros necessários.
    tabela = dynamodb.create_table(
        TableName=tabela_nome,
        KeySchema=[
            {
                'AttributeName': chave_particao_nome,
                'KeyType': 'HASH'  # HASH refere-se à chave de partição
            },
            {
                'AttributeName': chave_ordenacao_nome,
                'KeyType': 'RANGE'  # RANGE refere-se à chave de ordenação (sort key)
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': chave_particao_nome,
                'AttributeType': chave_particao_tipo
            },
            {
                'AttributeName': chave_ordenacao_nome,
                'AttributeType': chave_ordenacao_tipo
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Calma, é preciso esperar... a tabela está sendo montada.
    tabela.meta.client.get_waiter('table_exists').wait(TableName=tabela_nome)
    print(f"A belíssima tabela {tabela_nome} está pronta para o baile!")