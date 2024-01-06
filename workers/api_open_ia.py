import boto3
from botocore.config import Config
import logging
import os
from dotenv import load_dotenv
import requests
import json


load_dotenv(
    '/Users/fabioalvaropereira/workspaces/llm/llm-poc-antonio/config/.env')
logging.basicConfig(filename='/Users/fabioalvaropereira/workspaces/llm/llm-poc-antonio/workers/worker.log',
                    encoding='utf-8', level=logging.INFO)

# Cabeçalhos para a requisição
headers = {
    'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
    'Content-Type': 'application/json',
    'OpenAI-Beta': 'assistants=v1',
}


def openai_thread_busca_status(thread_id='', run_id=''):
    url_api = str(os.getenv("URL_OPENAI"))
    # Fazendo a requisição POST URL_OPENAI
    url = url_api + '/threads/'+thread_id+'/runs/'+run_id
    response = requests.get(url, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        logging.debug("   #200 openai_thread_busca_status")
        # logging.info(response.json())
        return response.json()
    else:
        logging.error("   #11 Falha ao openai_thread_busca_status")
        logging.error(
            f"Status Code: {response.status_code}, Response: {response.text}")
        return 'erro'


def openai_thread_submit_tool(thread_id='', run_id='', tool_call_id='', resposta=''):
    logging.debug(' envia submit tool ')
    logging.debug("assistant_id: " + str(os.getenv("ASSISTENTE_ID_VAR")))
    logging.debug("thread: " + str(thread_id))
    logging.debug("run_id: " + str(run_id))
    # Fazendo a requisição POST URL_OPENAI
    url = str(os.getenv("URL_OPENAI")) + '/threads/' + \
        thread_id+'/runs/'+run_id+'/submit_tool_outputs'
    print('url='+url)

    payload = {
        "tool_outputs": [
            {
                "tool_call_id": tool_call_id,
                "output": resposta
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        logging.debug("   submit ok")
        # logging.info(response.json())
        return response.json()
    else:
        logging.error("   #11 Falha ao submit tool")
        logging.error(
            f"Status Code: {response.status_code}, Response: {response.text}")
        return 'null'
