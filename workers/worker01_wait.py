import boto3
from botocore.config import Config
import logging
import os
import json
import requests
from dotenv import load_dotenv
from api_open_ia import openai_thread_busca_status, openai_thread_submit_tool

load_dotenv(
    '/Users/fabioalvaropereira/workspaces/llm/llm-poc-antonio/config/.env')
logging.basicConfig(filename='/Users/fabioalvaropereira/workspaces/llm/llm-poc-antonio/workers/worker.log',
                    encoding='utf-8', level=logging.INFO)

print('[worker1] >>> worker1 subiu !!!')
logging.info('[worker1] >>> worker1 subiu !!!')
# Configuração pra usar o LocalStack
localstack_url = 'http://localhost:4566'
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

headers = {
    'Content-Type': 'application/json'
}

# Configuração boto3
client_config = Config(
    region_name='us-east-1',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

if os.getenv("SQS") == 'LOCAL':
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
    sqs_client = boto3.client('sqs', config=client_config)

logging.info('[worker1] SQS='+str(os.getenv("SQS")))
print('[worker1] SQS='+str(os.getenv("SQS")))


# Nome da fila FIFO #SQS_FILA_GPT_ASSINCRONA
queue_name = str(os.getenv("SQS_FILA_01_AGUARDA_STATUS"))
print('[worker1] SQS_FILA_01_AGUARDA_STATUS='+str(queue_name))

try:
    # Pega a URL da fila
    response = sqs_client.get_queue_url(QueueName=queue_name)
    queue_url = response['QueueUrl']
except Exception as e:
    logging.error(f"Erro: {e}")


logging.info(
    "[worker1] WAIT_STATUS_WORKER Aguardando mensagens... Para interromper, pressione Ctrl+C")


def worker_1_cria_comando_3(thread_id, run_id, tool_call_id, output):
    url = 'http://localhost:8080/poc-azul/v1/teste/slot4'
    payload = {
        "dados": {
            "thread_id": thread_id,
            "run_id": run_id,
            "tool_call_id": tool_call_id,
            "output": output
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))


def recuperar_itens(url, thread_id, run_created):
    retorno = []
    payload9 = {
        "dados": {
            "thread_id": thread_id,
            "last_created": run_created
        }
    }
    try:
        response = requests.post(url9, headers=headers,
                                 data=json.dumps(payload9))
        # Se o status_code for 200, a requisição foi bem sucedida.
        if response.status_code == 201:
            itens = response.json()  # Supõe-se que a resposta seja um JSON.
            print(itens)
            retorno = itens
        else:
            print(f"Erro ao acessar a URL: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
    return retorno


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
                status_run = ''
                remove_da_fila = False
                # Processa a mensagem
                logging.info('')
                logging.info('**************************************')
                logging.info('Mensagem do comando 1 - WAIT_STATUS')
                body = json.loads(message['Body'])
                logging.info(body)
                logging.info('**************************************')
                thread_id = body['dados']['thread_id']
                run_id = body['dados']['run_id']

                retorno1 = openai_thread_busca_status(thread_id, run_id)

                status_run = retorno1['status']
                # logging.info('[worker1] FAKE VERIFICA STATUS DA THREAD!!!!')
                logging.info('thread_id='+thread_id +
                             ' | status_run='+status_run)

                if status_run == 'in_progress':
                    logging.info('status_run=in_progress')
                    # Nao faz nada apenas aguarda.
                if status_run == 'queued':
                    logging.info('status_run=queued')
                    # Nao faz nada apenas aguarda.

                if status_run == 'completed':
                    # tenho que pegar as mensagens que ainda nao enviei ate agora e enviar
                    # dentro da mensagem
                    mensagem = ''
                    run_created = body['dados']['run_created']
                    url9 = 'http://localhost:8080/poc-azul/v1/teste/slot9'

                    lista = recuperar_itens(url9, thread_id, run_created)

                    if len(lista) > 0:

                        for item in lista:
                            mensagem = mensagem + \
                                item['content'][0]['text']['value']

                    # ===============

                    # mensagem = ' preciso definir aqui no worker 1 WAIT, deveria vir pelo comando ne?'
                    logging.info('[worker1]wait status_run=completed')
                    destino = body['dados']['telefone']

                    # SE status_run_banco é diferente de completed
                    # envia comando 2 - concluido/whatsapp
                    url = 'http://localhost:8080/poc-azul/v1/teste/slot5'
                    payload = {"dados": {
                        "mensagem": mensagem,
                        "destino": destino
                    }}
                    response = requests.post(
                        url, headers=headers, data=json.dumps(payload))
                    logging.info(response)
                    if response.status_code == 400:
                        logging.info(response.json['error'])
                    if response.status_code == 201:
                        logging.info(
                            'worker1_wait >> comando2_concluido enviado com sucesso')
                        logging.info(payload)
                        remove_da_fila = True
                    # muda status no banco
                    # Remove a mensagem da fila

                # if status_run=='requires_action':
                #   logging.info ('status_run=requires_action')
                #   #SE status_run_banco é diferente de requires_action

                #   tool_call_id = retorno1['required_action']['submit_tool_outputs']['tool_calls'][0]['id']
                #   logging.info ('tool_call_id='+tool_call_id)
                #   # envia comando 3
                #   retorno_api = ' agendamento_codigo: 23632;data:15-01-2024;horario:17:00;Vistoriador_remoto:Denilson Silva;sucesso: true'
                #   worker_1_cria_comando_3(thread_id,run_id,tool_call_id,retorno_api)
                #   # muda status no banco
                #   # Remove a mensagem da fila
                #   remove_da_fila=True

                if status_run == 'expired':
                    logging.info('[worker1] status_run=expired')
                    # SE status_run_banco é diferente de expired
                    # Remove a mensagem da fila depois precisa enviar uma mensagem e entender melhor o fluxo #TODO
                    remove_da_fila = True

                if (remove_da_fila == True):
                    # Deleta a mensagem da fila após processá-la
                    sqs_client.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    logging.info(
                        f"[worker1] Mensagem verifica status da thread foi Removida da fila: {message['ReceiptHandle']}")
        else:
            # Se não há mensagens, o loop continua
            logging.info("[worker1] Nenhuma mensagem nova.")
except KeyboardInterrupt:
    logging.error("[worker1] \nInterrompido pelo usuário.")
