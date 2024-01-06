import boto3
from botocore.config import Config
import logging
import os
import json
from dotenv import load_dotenv
import requests
from api_open_ia import openai_thread_busca_status,openai_thread_submit_tool

load_dotenv('../config/.env')
logging.basicConfig(filename='worker.log', encoding='utf-8', level=logging.INFO)

print('[worker3] >>> WORKER 3 WAit_action subiu !!!')
logging.info('[worker3] >>> WORKER 3 WAit_action subiu  !!!')
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

headers = {
    'Content-Type': 'application/json'
}



if os.getenv("SQS")=='LOCAL':    
    # Cria o cliente SQS apontando para o LocalStack
    sqs_client = boto3.client(
        'sqs',
        endpoint_url=localstack_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=client_config
    )
else:
    # Cria o cliente SQS apontando para o LocalStack
    sqs_client = boto3.client('sqs',config=client_config)
    
logging.info('[worker3] SQS='+str(os.getenv("SQS")))
print('[worker3] SQS='+str(os.getenv("SQS")))


# Nome da fila FIFO #SQS_FILA_GPT_ASSINCRONA
queue_name = str(os.getenv("SQS_FILA_03_WAIT_ACTION"))

logging.info('[worker3] SQS_FILA_03_WAIT_ACTION='+str(queue_name))
print('[worker3] SQS_FILA_03_WAIT_ACTION='+str(queue_name))

try:
    # Pega a URL da fila
    response = sqs_client.get_queue_url(QueueName=queue_name)
    queue_url = response['QueueUrl']
    print(queue_url)

except Exception as e:
    logging.error(f"Erro: {e}")
    
    
logging.info("[worker3] Aguardando mensagens... Para interromper, pressione Ctrl+C")

try:
    while True:
        # Recebe mensagens da fila com uma espera longa
        messages = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )

        if 'Messages' in messages:
            for message in messages['Messages']:
                # Processa a mensagem
                logging.info('')          
                body = json.loads(message['Body'])
                logging.info(body) 
                
                thread_id=body['dados']['thread_id']
                run_id=body['dados']['run_id']
                tool_call_id =body['dados']['tool_call_id']
                telefone=body['dados']['telefone']
                assistant_id=body['dados']['assistant_id']
                # FARIA UMA CONSULTA A API DO CLIENTE DE AGENDAMENTO...... #TODO
                output=body['dados']['output']
   
                url = 'http://localhost:8080/poc-azul/v1/teste/slot4'
                payload={
                            "dados": {
                                "thread_id": thread_id,
                                "run_id": run_id,
                                "tool_call_id": tool_call_id,
                                "output": output
                            }
                        }
                response = requests.post(url, headers=headers,data=json.dumps(payload))     
                logging.info("     aaaaaaaaaaaaaaaaaaaaaaaa aaaaaa aaaaaaa")
                logging.info(    response )
                if response.status_code==400:
                  logging.info (response.json['error'])
                if response.status_code in [200,201]:
                  logging.info("     aaaaaaaaaaaaaaa!!!!!       Apos a chamada assincrona rodar o assistente novamente....")
                  url2 = 'http://localhost:8080/poc-azul/v1/teste/slot7'
                  payload2={
                            "dados": {
                                "thread_id": thread_id,
                                "telefone": telefone,
                                "assistant_id": assistant_id
                            }
                        }
                  response2 = requests.post(url2, headers=headers,data=json.dumps(payload2))
                
                  
                    
                
                #logging.info ( response)
                
                if (1==1):
                  # Deleta a mensagem da fila após processá-la
                  sqs_client.delete_message(
                       QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                   )
                  logging.info(f"[worker] Comando3 de submit-tool foi removido da  fila: {message['ReceiptHandle']}")
        else:
            # Se não há mensagens, o loop continua
            logging.info("[worker3] Nenhuma mensagem nova.")
except KeyboardInterrupt:
    logging.error("[worker3] \nInterrompido pelo usuário.")