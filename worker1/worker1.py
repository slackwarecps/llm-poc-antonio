import boto3
from botocore.config import Config
import logging
import os
import json
from dotenv import load_dotenv
from api_open_ia import openai_thread_busca_status,openai_thread_submit_tool

load_dotenv('../config/.env')
logging.basicConfig(filename='worker.log', encoding='utf-8', level=logging.INFO)

print('[worker] >>> WORKER subiu !!!')
logging.info('[worker] >>> WORKER subiu !!!')
# Configuração pra usar o LocalStack
localstack_url = 'http://localhost:4566'
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

# Configuração boto3
client_config = Config(
    region_name='us-east-1',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# Cria o cliente SQS apontando para o LocalStack
sqs_client = boto3.client(
    'sqs',
    endpoint_url=localstack_url,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    config=client_config
)

# Nome da fila FIFO
queue_name = 'sqs_batata.fifo'

try:
    # Pega a URL da fila
    response = sqs_client.get_queue_url(QueueName=queue_name)
    queue_url = response['QueueUrl']

    # Recebe mensagens da fila
    messages = sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=10,
        WaitTimeSeconds=5
    )

    # # Checagem se há mensagens
    # if 'Messages' in messages:
    #     for message in messages['Messages']:
    #         # Processa a mensagem
    #         logging.info(f"[worker] Mensagem recebida: {message['Body']}")
    #         logging.info('[worker] Enviar mensagem ')
    #         # Deleta a mensagem da fila para evitar reprocessamento
    #         sqs_client.delete_message(
    #             QueueUrl=queue_url,
    #             ReceiptHandle=message['ReceiptHandle']
    #         )
    # else:
    #     logging.info("[worker] Nenhuma mensagem nova na fila.")

except Exception as e:
    logging.error(f"Erro: {e}")
    
    
logging.info("[worker] Aguardando mensagens... Para interromper, pressione Ctrl+C")

try:
    while True:
        # Recebe mensagens da fila com uma espera longa
        messages = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        if 'Messages' in messages:
            for message in messages['Messages']:
                # Processa a mensagem
                logging.info('')
                #logging.info(f"[worker] Mensagem recebida: {message['Body']}")
                #logging.info(message)                
                body = json.loads(message['Body'])
                
                thread_id=body['dados']['thread_id']
                run_id=body['dados']['run_id']
                
                retorno1 = openai_thread_busca_status(thread_id,run_id)
                if 'status' in retorno1:
                  status_run=retorno1['status']
                else:
                  status_run='erro'
                # logging.info('Status da Thread: '+status_run)
                logging.info('status_run='+status_run) 
                
                
                if status_run=='requires_action':
                  logging.info(' >>>>>>>>>> requires_action <<<<<<<<<<<<')
                  tool_call_id =retorno1['required_action']['submit_tool_outputs']['tool_calls'][0]['id']
                  logging.info( retorno1['required_action']['submit_tool_outputs']['tool_calls'][0]['id']       )
                  retorno2 =openai_thread_submit_tool(thread_id,run_id,tool_call_id)
                  logging.info ( retorno2)
                  
                #if (status_run=='completed'):
                
                if (status_run=='completed'):
                  # Deleta a mensagem da fila após processá-la
                  sqs_client.delete_message(
                       QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                   )
                  logging.info(f"[worker] Mensagem apagada da fila: {message['ReceiptHandle']}")
        else:
            # Se não há mensagens, o loop continua
            logging.info("[worker] Nenhuma mensagem nova.")
except KeyboardInterrupt:
    logging.error("[worker] \nInterrompido pelo usuário.")