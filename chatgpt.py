# chatgpt.py
import requests
import uuid
import logging
import json
import os
from dotenv import load_dotenv
import time
from services.sqs import sqs_enviar


debug = False
load_dotenv('config/.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Endpoint da GPT-4 API
url_api = 'https://api.openai.com/v1'
# 'asst_Z1pMBbuDlAQLLJ0nyTMttgHl'
ASSISTENTE_ID_VAR = os.getenv("ASSISTENTE_ID_VAR")

# Cria um identificador único para a sessão da conversa
session_id = str(uuid.uuid4())

# Cabeçalhos para a requisição
headers = {
    'Authorization': f'Bearer {OPENAI_API_KEY}',
    'Content-Type': 'application/json',
    'OpenAI-Beta': 'assistants=v1',
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location.",
                    },
                },
                "required": ["location", "format"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_n_day_weather_forecast",
            "description": "Get an N-day weather forecast",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location.",
                    },
                    "num_days": {
                        "type": "integer",
                        "description": "The number of days to forecast",
                    }
                },
                "required": ["location", "format", "num_days"]
            },
        }
    },
]


def func_gpt_criar_thread():
    logging.info("name: " + __name__)
    logging.info(' #4 Entrou na func_gpt_criar_thread')

    # Fazendo a requisição POST
    url = url_api + '/threads'
    response = requests.post(url, headers=headers)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Extraindo a resposta
        response_data = response.json()
        # A resposta do chat pode ser encontrada em 'choices'
        # chat_response = response_data.get('choices', [{}])[0].get('text', '').strip()
        # print(response_data)
        logging.info(' #4 thread criada no chatgpt')
        return response_data
    else:
        logging.error(f"Erro ao fazer a requisição: {response.status_code}")
        return 'null'


def func_gpt_criar_mensagem(thread_id, mensagem):
    logging.info("name: " + __name__)
    logging.info(' #5 chatgpt.func_gpt_criar_mensagem ')
    payload = {
        "role": "user",
        "content": mensagem
    }
    # Fazendo a requisição POST
    url = url_api + '/threads/'+thread_id+'/messages'
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    retorno1 = response.json()
    # logging.info("status_code="+str(response.status_code))
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        logging.info("   #5 51 Mensagem criada com sucesso no chat gpt.")
        return response.json()
    else:
        logging.error("   #5 51 Falha ao chatgpt.func_gpt_criar_mensagem.")
        logging.error(
            f"Status Code: {response.status_code}, Response: {response.text}")
        logging.error(retorno1['error']['message'])
        if (deve_processa_novamente(retorno1['error']['message']) == True):
            logging.error(' ')
            logging.error(
                'x xxxxxxxx xxxxxxxx xxxxx SIM VAI RE-PROCESSAR local:criar mensagem xxxxxxxxxxxx')
            logging.error(' ')
            logging.error(' ')
            # func_gpt_rodar_assistente(response['thread_id'],telefone,assistant_id)
            return 're-processar'
        else:
            return 'null'


def deve_processa_novamente(MensagemDeErro):
    retorno = False
    phrase = 'already has an active run '
    phrase2 = ' while a run '

    if phrase in MensagemDeErro:
        retorno = True
    if phrase2 in MensagemDeErro:
        retorno = True
    return retorno


def func_gpt_rodar_assistente(thread_id, telefone='', assistant_id='', beta=[]):

    logging.debug(' #9 Entrou na chatgpt.func_gpt_rodar_assistente')
    logging.debug("     thread: " + str(thread_id))
    logging.debug('     telefone='+telefone)
    logging.debug('     assistant_id='+assistant_id)
    logging.debug('     beta=')
    logging.debug(beta)
    if assistant_id == '':
        assistant_id = ASSISTENTE_ID_VAR
        logging.debug('usando o default ASSISTENTE_ID_VAR='+ASSISTENTE_ID_VAR)

    if telefone in beta:
        logging.debug('assistant_id='+assistant_id)
        payload = {"assistant_id": 'asst_8TumJSDdiN6xoPczLr4MktAu'}
        logging.debug("ASSISTENTE_ID: Bugiganga!!!xxxx")
    else:
        payload = {"assistant_id": assistant_id}
        logging.debug("ASSISTENTE_ID: "+assistant_id)

    # Fazendo a requisição POST
    url = url_api + '/threads/'+thread_id+'/runs'
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    retorno1 = response.json()
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        logging.info("   #9 chatgpt.func_gpt_rodar_assistente")
        # logging.info(retorno1)
        return response.json()
    else:
        logging.error("   #9 Falha ao chatgpt.func_gpt_rodar_assistente")
        logging.error(
            f"Status Code: {response.status_code}, Response: {response.text}")
        logging.error(retorno1['error']['message'])
        return 'null'


# RODA O ALGORITIMO DO CHATGPT RUN
# 'expired','in_progress','completed'
def func_gpt_status_do_run_do_assistente(thread_id, run_id):
    logging.info(' #11 Entrou na func_gpt_status_do_run_do_assistente ')
    logging.info("assistant_id: " + ASSISTENTE_ID_VAR)
    logging.info("thread: " + str(thread_id))
    # Fazendo a requisição POST
    url = url_api + '/threads/'+thread_id+'/runs/'+run_id
    response = requests.get(url, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        logging.info("   #11 CHATGPT RUN")
        # logging.info(response.json())
        return response.json()
    else:
        logging.error("   #11 Falha ao CHATGPT RUN")
        logging.error(
            f"Status Code: {response.status_code}, Response: {response.text}")
        return 'null'


# Busca Mensagens da Thread
def func_gpt_busca_mensagens(thread_id=''):
    logging.info(' #15 Entrou na func_gpt_busca_mensagens ')
    logging.info("thread: " + thread_id)
    # Fazendo a requisição POST
    url = url_api + '/threads/'+thread_id+'/messages'
    response = requests.get(url, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        logging.info("   #15 busca_mensagens realizada com sucesso ")
        # logging.info(response.json())
        return response.json()
    else:
        logging.error("   #15 Falha ao busca_mensagens")
        logging.error(
            f"Status Code: {response.status_code}, Response: {response.text}")
        return 'null'


def func_gpt_busca_runs_ativas(thread_id=''):
    logging.debug(' Entrou na chatgpt.func_gpt_busca_runs_ativas ')
    logging.debug("thread: " + thread_id)
    # Fazendo a requisição POST
    url = url_api + '/threads/'+thread_id+'/runs'
    response = requests.get(url, headers=headers)
    retorno = response.json

    lista = []

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        logging.debug("   chatgpt.func_gpt_busca_runs_ativas com sucesso ")
        # for item in data2:
        retorno = response.json()
        resposta = {}
        # logging.info(retorno['data'])
        for run in retorno['data']:
            if run['status'] not in ['expired', 'completed']:
                tool_calls_id = run['required_action']['submit_tool_outputs']['tool_calls'][0]['id']
                item = {"run_id": run['id'],
                        "status": run['status'], "call_id": tool_calls_id}
                lista.append(item)

            # logging.info(run['id']+' | '+run['status'])

        # logging.info(resposta)
        return lista
    else:
        logging.error("   Falha ao chatgpt.func_gpt_busca_runs_ativas")
        logging.error(
            f"Status Code: {response.status_code}, Response: {response.text}")
        return 'null'


def func_gpt_submit_tool(thread_id='', run_id='', tool_call_id='', output=''):
    logging.info('>>> func_gpt.func_gpt_submit_tool')

    payload = {
        "tool_outputs": [
            {
                "tool_call_id": tool_call_id,
                "output": output
            }
        ]
    }
    # Fazendo a requisição POST
    url = url_api + '/threads/'+thread_id+'/runs/'+run_id+'/submit_tool_outputs'

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(">>> Falha func_gpt.func_gpt_submit_tool")
        # logging.error(f"Status Code: {response.status_code}, Response: {response.text}")
        return 'null'
