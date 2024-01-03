from flask import Flask, request, redirect, url_for,jsonify

import chatgpt
from chatgpt import func_gpt_submit_tool
from chatgpt import func_gpt_busca_mensagens
from controllers.twiliox import func_responde_ao_cliente_pelo_whatsapp
from controllers.twiliox import dynamo_thread_todos,dynamo_mensagem_salvar
from controllers.twiliox import dynamo_clientes_todos,dynamo_parametro_todos,dynamo_clientes_updatebyId,dynamo_execucao_todos
import logging
from controllers.twiliox import func_twilio_chegou
from services.parametro.service_parametro import func_parametros_busca_todos
from services.api_azul_agendamentos import agendamento_cancelar

import os
from dotenv import load_dotenv
import time
from flask_cors import CORS
import socketio
from services.sqs import sqs_enviar_mensagem,sqs_enviar_comando_3,sqs_enviar_comando_2,sqs_enviar_comando_1
import uuid
import json
#import globais


load_dotenv('config/.env')



logging.basicConfig(filename='log/poc-azul.log', encoding='utf-8', level=logging.INFO)
logging.debug('aplicacao iniciada')
logging.debug(' ')
logging.debug('****************************************')

api='/poc-azul/v1/'
api_bff='/bff/v1/'

# Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})




@app.route('/', methods=['GET'])
def home():
 
  logging.info('chegou na home page!')
  logging.info('AMBIENTE=' + os.getenv("AMBIENTE"))
  return '<h1> POC AZUL v1.0</h1>'+'<br>Ambiente='+ os.getenv("AMBIENTE"), 200

@app.route('/teste', methods=['GET'])
def teste():

  logging.info('TESTE')
  #dynamo_thread_update_UltimaRespostaByTelefone("5511983477360", 1234)
  dynamo_mensagem_salvar("5519981857976","thread_h0tWPIgEucMek0aNRTbrdGVq","alguma coisa")

  #func_gpt_busca_mensagens(os.getenv("T_THREAD"))
  return 'Teste v1.0', 200



# twilio chamadas

@app.route(api+'comunicacao/chegou', methods=['POST'])
def chegou():
  logging.info('vai enviar a mensagem no whats')
  SmsMessageSid = request.form.get('SmsMessageSid')
  wa_id = request.form.get('WaId')
  logging.info('tel_origem='+wa_id)
  logging.info('SmsMessageSid='+SmsMessageSid)
  func_twilio_chegou(request)
  return 'OK mesmo 3', 201






@app.route(api+'comunicacao/health', methods=['GET'])
def health():
  return 'health', 200





# frontend chamadas

@app.route(api+'bff/conversa', methods=['GET'])
def funcao():
  chatgpt.funcao_01()
  return 'chamou a funcao 01', 200

@app.route(api+'bff/conversa/<int:id>/modo', methods=['POST'])
def funcao2(id):
  chatgpt.funcao_02()
  return str(id)+' modo da conversa alterado : Assistente desligado', 201

@app.route(api+'bff/parametro', methods=['POST'])
def funcao3():
  chatgpt.funcao_03()
  return 'parametro do sistema modificado ', 201


# Whatsapp Service twilio Callbacks
@app.route(api+'service/request', methods=['POST'])
def service_request():
  logging.info('POST >> no service_request')
  return '', 201

@app.route(api+'service/fallback', methods=['POST'])
def service_fallback():
  logging.info('POST >> no service_fallback')
  return '', 201

@app.route(api+'service/health', methods=['GET'])
def service_health():
  logging.info('GET >> no service_health')
  message_sid = request.values.get('MessageSid', None)
  message_status = request.values.get('MessageStatus', None)
  logging.info('SID: {}, Status: {}'.format(message_sid, message_status))

  return ('', 204)

####
### TESTES, sim depois pode apagar isso aqui :) #to-do
####
@app.route(api+'teste/slot1', methods=['GET'])
def teste_slot1():
  logging.info('GET >> teste/slot1')
  retorno = agendamento_cancelar(26721993880,'Estou de ferias')
  logging.info(retorno)
  logging.info('=============================')
  return (retorno, 201)

@app.route(api+'teste/slot2', methods=['POST'])
def teste_slot2():
  gerado_uuid = str(uuid.uuid4() )
  
  data_json = request.get_json()
  logging.info('POST >> teste/slot2')
  
  logging.info(data_json)
  objeto = {
    'uuid':gerado_uuid,
    'data':data_json['data'],
    'horario':data_json['horario'],
    'vistoriador_remoto': data_json['vistoriador_remoto'],
    'dados':data_json['dados']
    }
  
  retorno = sqs_enviar_mensagem(objeto)
  
  logging.info('=============================')
  return (retorno, 201)

@app.route(api+'teste/slot3', methods=['POST'])
def teste_slot3():
  
  data_json = request.get_json()
  logging.info('POST >> teste/slot3')
  
  logging.info(data_json)
  objeto = {
    'dados':data_json['dados']
    }
  
  retorno = sqs_enviar_comando_3(objeto)
  
  logging.info('=============================')
  return (retorno, 201)


@app.route(api+'teste/slot4', methods=['POST'])
def teste_slot4():
  
  data_json = request.get_json()
  logging.info('POST >> teste/slot4')
  
  logging.info(data_json)
  objeto = {
    'dados':data_json['dados']
    }
  
  retorno = func_gpt_submit_tool(data_json['dados']['thread_id'],
                                 data_json['dados']['run_id'],
                                 data_json['dados']['tool_call_id'],
                                 data_json['dados']['output']
                                 )
  
  logging.info('=============================')
  return (retorno, 201)

@app.route(api+'teste/slot5', methods=['POST'])
def teste_slot5():
  
  data_json = request.get_json()
  logging.info('POST >> teste/slot5')
  
  logging.info(data_json)
  objeto = {
    'dados':data_json['dados']
    }
  
  retorno = sqs_enviar_comando_2(objeto)
  
  logging.info('=============================')
  return (retorno, 201)

@app.route(api+'teste/slot6', methods=['POST'])
def teste_slot6():
  
  data_json = request.get_json()
  logging.info('POST >> teste/slot6')
  
  logging.info(data_json)
  objeto = {
    'dados':data_json['dados']
    }
  
  retorno = sqs_enviar_comando_1(objeto)
  
  logging.info('=============================')
  return (retorno, 201)


####
### BFF Angular
#### front /bff/v1/chats
@app.route(api_bff+'chats', methods=['GET'])
def bff_chats():
  #logging.info(' #bff front /bff/v1/chats')
  retorno = dynamo_thread_todos()  
  return (retorno, 200)




####
### BFF Angular
#### front /bff/v1/chats/1
@app.route(api_bff+'chats/<string:telefone>', methods=['GET'])
def bff_chats_by_telefone(telefone):
  #logging.info(' >>>>> BFF func_bff_chats telefone='+ telefone)
  #retorno = func_bff_chatsByTelefone(telefone)
  return ('teste123', 200)

####
### BFF CHAT por id
#### front /bff/v1/chats-by-id/thread_4q2SaBanQRRigbyVpgaWoKmr
@app.route(api_bff+'chats-by-id/<string:id>', methods=['GET'])
def bff_chats_by_telefonexxx(id):
  #logging.info(' >>>>> BFF chats-by-id='+ id)
  retorno = func_gpt_busca_mensagens(id)
  return (retorno, 200)


####
### BFF Clientes TODOS
#### front /bff/v1/chats-by-id/thread_4q2SaBanQRRigbyVpgaWoKmr
@app.route(api_bff+'clientes', methods=['GET'])
def bff_clientes_todos():
  #logging.info(' >>>>> BFF clientes')
  retorno = dynamo_clientes_todos()
  return (retorno, 200)
####
### BFF Execucao TODOS
#### front /bff/v1/execucao
@app.route(api_bff+'execucao', methods=['GET'])
def bff_execucao_todos():
  #logging.info(' >>>>> BFF execucao')
  retorno = dynamo_execucao_todos()
  return (retorno, 200)

####
### BFF Cliente por Telefone UPDATE
#### front /bff/v1/clientes/11983477360
@app.route(api_bff+'clientes/<string:telefone>', methods=['PUT'])
def bff_clientes_update(telefone):
  logging.info(' >>>>> BFF bff_clientes_update'+telefone)
  # Obtém o body da requisição em formato JSON
  data = request.get_json()
  # Verifica se 'nome' e 'valor' estão presentes no body
  if 'telefone' not in data or 'modo_assistente' not in data:
      return jsonify({'message': 'telefone e modo_assistente são obrigatórios.'}), 400
   # Extrai 'nome' e 'valor' do body da requisição
  telefone = data['telefone']
  modo = data['modo_assistente']
  retorno = dynamo_clientes_updatebyId(telefone,modo)
  #logging.info(retorno)
  # Como exemplo, vamos apenas retorná-los
  return jsonify({'telefone': telefone, 'modo_assistente': modo}), 201


####
### BFF Angular
#### front /bff/v1/parametro
@app.route(api_bff+'parametro', methods=['GET'])
def bff_parametro():
  #logging.info(' >>>>> BFF parametro')
  retorno = dynamo_parametro_todos()
  return (retorno, 200)


if __name__ == "__main__":

  
  # retorno = func_parametros_busca_todos()
  # print(retorno)
  # # Aqui está nossa caixa de ferramentas, quero dizer, nossa lista de strings
  # lista_de_valores = retorno['Items'][0]['numeros_beta_fabio']

  # # E aqui está o parafuso que estamos procurando... ops, a string que queremos verificar
  # string_procurada = "5511983477360"
  # #print(retorno['Items']['numeros_beta_fabio'])
  # #if '5511983477360' in retorno['Items']['numeros_beta_fabio']:
  # if string_procurada in lista_de_valores:
  #   print(f"Achei! O '{string_procurada}' está bem aqui na lista!")
  # else:
  #   print(f"Não achei! O '{string_procurada}' deve ter saído para dar uma volta.")
  # Cria um cliente SocketIO

  uri='http://ec2-54-91-43-205.compute-1.amazonaws.com'
  #globais.sio.connect('http://localhost:8091')

  

  print('AMBIENTE='+os.getenv("AMBIENTE"))
  print('BANCO='+os.getenv("BANCO"))
  print('SQS='+os.getenv("SQS"))
  print('VERSAO_LOGICA='+os.getenv("VERSAO"))
  print('PROJETO='+os.getenv("PROJETO"))
  
  print('ASSISTENTE_ID_VAR='+os.getenv("ASSISTENTE_ID_VAR"))
  app.run(host="0.0.0.0", port=int("8080"), debug=True)

