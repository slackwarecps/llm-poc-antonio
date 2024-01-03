import boto3
from botocore.config import Config
import logging
import os
from dotenv import load_dotenv
import requests
import json


load_dotenv('../config/.env')
logging.basicConfig(filename='worker.log', encoding='utf-8', level=logging.INFO)

# Cabeçalhos para a requisição
headers = {
    'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
    'Content-Type': 'application/json',
    'OpenAI-Beta': 'assistants=v1',
}

def openai_thread_busca_status(thread_id='',run_id=''):
  logging.info(' #11 Entrou na func_gpt_status_do_run_do_assistente ') 
  logging.info("assistant_id: "+ str( os.getenv("ASSISTENTE_ID_VAR")))
  logging.info("thread: "+ str(thread_id))
  # Fazendo a requisição POST URL_OPENAI
  url = str(os.getenv("URL_OPENAI")) + '/threads/'+thread_id+'/runs/'+run_id
  print(url)
  response = requests.get(url, headers=headers)

  # Verifica se a requisição foi bem-sucedida
  if response.status_code == 200:
    logging.info("   #200 openai_thread_busca_status")
    #logging.info(response.json())
    return response.json()
  else:
    logging.error("   #11 Falha ao openai_thread_busca_status")
    logging.error(f"Status Code: {response.status_code}, Response: {response.text}")
    return 'erro'





def openai_thread_submit_tool(thread_id='',run_id='',tool_call_id='',resposta=''):
  logging.info(' envia submit tool ') 
  logging.info("assistant_id: "+ str( os.getenv("ASSISTENTE_ID_VAR")))
  logging.info("thread: "+ str(thread_id))
  logging.info("run_id: "+ str(run_id))
  # Fazendo a requisição POST URL_OPENAI
  url = str(os.getenv("URL_OPENAI")) + '/threads/'+thread_id+'/runs/'+run_id+'/submit_tool_outputs'
  print('url='+url)
  
  payload = {
     "tool_outputs": [
        {
            "tool_call_id": tool_call_id,
            "output": resposta
        }
    ]
  }
   
  response = requests.post(url, headers=headers,data=json.dumps(payload))

  # Verifica se a requisição foi bem-sucedida
  if response.status_code == 200:
    logging.info("   submit ok")
    #logging.info(response.json())
    return response.json()
  else:
    logging.error("   #11 Falha ao submit tool")
    logging.error(f"Status Code: {response.status_code}, Response: {response.text}")
    return 'null'





print('Rodou api teste')
thread_id='thread_3I6n1VOVwL7hRLl8x9uoFRz4'
run_id='run_i0UoqikH8lpLvuWpBSeQCJOR'
retorno = openai_thread_busca_status(thread_id,run_id)
print ( retorno['status'])

if retorno['status']=='requires_action':
  tool_call_id =retorno['required_action']['submit_tool_outputs']['tool_calls'][0]['id']
  print( retorno['required_action']['submit_tool_outputs']['tool_calls'][0]['id']       )
  retorno2 =openai_thread_submit_tool(thread_id,run_id,tool_call_id)
  print ( retorno2)
  

retorno3 = openai_thread_busca_status(thread_id,run_id)
print ( retorno3['status'])
