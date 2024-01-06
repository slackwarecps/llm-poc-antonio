import boto3
from botocore.config import Config
import json
import os
from dotenv import load_dotenv
import logging
import uuid


def sqs_enviar(corpo, fila=''):
    load_dotenv('../config/.env')
    logging.basicConfig(filename='../log/poc-azul.log',
                        encoding='utf-8', level=logging.INFO)
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
    if os.getenv("SQS") == 'LOCAL':
        # Preparar o cliente SQS pra apontar pro LocalStack
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
    # Nome da fila FIFO

    # queue_name = str(os.getenv("SQS_FILA_GPT_ASSINCRONA"))
    queue_name = fila

    mensagem = corpo
    gerado_uuid = str(uuid.uuid4())
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
            MessageGroupId='batata_grupo',  # agrupar pelo telefone
            # E um ID de deduplicação, mesmo com deduplicação baseada em conteúdo
            MessageDeduplicationId=gerado_uuid
        )
        # Sucesso na passarela!
        logging.info(f"Mensagem inserida da fila "+queue_url +
                     " com sucesso! ID da mensagem:" + str({response_envio['MessageId']}))

    except Exception as e:
        # Se a batata não puder dançar...
        logging.error(f"Erro ao enviar mensagem: {e}")


# Fila de aguardar status worker1
def sqs_enviar_mensagem(objeto):
    fila = str(os.getenv("SQS_FILA_GPT_ASSINCRONA"))
    logging.info('>> sqs.sqs_enviar_mensagem comando 1 status aguarda')
    logging.info(objeto)
    sqs_enviar(objeto, fila)

    return 'sucesso ' + str(objeto)

# SQS_FILA_01_AGUARDA_STATUS=sqs_concluido.fifo


def sqs_enviar_comando_1(objeto):
    fila = str(os.getenv("SQS_FILA_01_AGUARDA_STATUS"))
    logging.debug('>> sqs.sqs_enviar_comando_1_aguarda')
    logging.debug(objeto)
    sqs_enviar(objeto, fila)

    return 'sucesso ' + str(objeto)


# SQS_FILA_02_CONCLUIDO=sqs_concluido.fifo
def sqs_enviar_comando_2(objeto):
    fila = str(os.getenv("SQS_FILA_02_CONCLUIDO"))
    logging.info('>> sqs.sqs_enviar_comando_2_concluido')
    logging.info(objeto)
    sqs_enviar(objeto, fila)

    return 'sucesso ' + str(objeto)

# SQS_FILA_03_WAIT_ACTION=sqs_wait_action.fifo


def sqs_enviar_comando_3(objeto):
    fila = str(os.getenv("SQS_FILA_03_WAIT_ACTION"))
    logging.info('>> sqs.sqs_enviar_comando_3_wait')
    logging.info(objeto)
    sqs_enviar(objeto, fila)
    return 'sucesso ' + str(objeto)
