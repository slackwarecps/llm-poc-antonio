import boto3
from botocore.config import Config
import json
import os
from dotenv import load_dotenv
import logging
import uuid

def sqs_enviar(corpo):
  
    load_dotenv('../config/.env')
    logging.basicConfig(filename='../log/poc-azul.log', encoding='utf-8', level=logging.INFO)


    # Configuração pro LocalStack
    localstack_url = 'http://localhost:4566'
    aws_access_key_id = 'test'
    aws_secret_access_key = 'test'

    # Configuração do boto3
    client_config = Config(
        region_name='us-east-1',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )

    # Preparar o cliente SQS pra apontar pro LocalStack
    sqs_client = boto3.client(
        'sqs',
        endpoint_url=localstack_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=client_config
    )

    # Nome da fila FIFO
    queue_name = 'sqs_batata.fifo'
    

 


    # Vamos preparar a nossa "batata corrida", com um código e um comentário
    # mensagem = {
    #     "codigo": "B123",
    #     "comentario": "Uma batata muito bonita",
    #     "tool_call_id":"call_abc123",
    #     "output":'''agendamento_codigo": 2632,
    #         "data": "15-01-2024",
    #         "horario": "17:00",
    #         "Vistoriador_remoto": "Denilson Silva'''
    # }
    mensagem=corpo
 
    gerado_uuid = str(uuid.uuid4() )

    # E agora, essa batata precisa de uma roupa de gala, o JSON
    mensagem_json = json.dumps(mensagem)
          
    try:
        # Pegar URL da fila - esse é o passo elegante antes do grande baile
        response = sqs_client.get_queue_url(QueueName=queue_name)
        queue_url = response['QueueUrl']

        # Envio da batata VIP
        response_envio = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=mensagem_json,  # Aqui vai a mensagem no tapete vermelho
            MessageGroupId='batata_grupo',  # As batatas FIFO precisam de um ID de grupo
            MessageDeduplicationId=gerado_uuid  # E um ID de deduplicação, mesmo com deduplicação baseada em conteúdo
        )

        # Sucesso na passarela!
        logging.info(f"Mensagem inserida da fila "+queue_url+" com sucesso! ID da mensagem:"+ str({response_envio['MessageId']}) )

    except Exception as e:
        # Se a batata não puder dançar...
        logging.error(f"Erro ao enviar mensagem: {e}")

def sqs_enviar_mensagem(objeto):
    logging.info('Enviar mensagem ')
    logging.info(objeto)
    sqs_enviar(objeto)
    
    return 'sucesso '+ str(objeto)