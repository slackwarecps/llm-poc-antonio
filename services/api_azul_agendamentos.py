import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr

from botocore.exceptions import ClientError
from pprint import pprint
from datetime import datetime
import pytz
import time
from chatgpt import func_gpt_criar_thread
from chatgpt import func_gpt_criar_mensagem
from chatgpt import func_gpt_rodar_assistente
from chatgpt import func_gpt_status_do_run_do_assistente
from chatgpt import func_gpt_busca_mensagens

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv('../config/.env')
VERSAO=os.getenv("VERSAO","V1")


def agendamento_cancelar(agendamento_id=0, motivo=''):
    logging.info('api agendamento cancelar')
    retorno = {
        'agendamento_id': agendamento_id,
        'motivo': motivo,
        'sucesso':True
    }
    return retorno