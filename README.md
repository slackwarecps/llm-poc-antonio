# poc-laranja-chatgpt
Uso de AI generativa com a api do whatsapp para uma poc de integração. #Software  3.0 asdasdasd

# thread
```
{
  "messages": [
    {
      "thread_id": "thread_CqbkLwvNZkyc3gv7YGOVDfHL",
      "metadata": {},
      "role": "user",
      "assistant_id": null,
      "run_id": null,
      "file_ids": [],
      "created_at": 1701682100,
      "id": "msg_yFKL4XG63tEJjHLFQH1SYCNc",
      "content": [
        {
          "type": "text",
          "text": {
            "value": "quero uma piada bem ruim sobre um pato amarelo",
            "annotations": []
          }
        }
      ],
      "object": "thread.message"
    },
    {
      "thread_id": "thread_CqbkLwvNZkyc3gv7YGOVDfHL",
      "metadata": {},
      "role": "user",
      "assistant_id": null,
      "run_id": null,
      "file_ids": [],
      "created_at": 1701682162,
      "id": "msg_DaMoFjrmEPUJB85oCuG584ry",
      "content": [
        {
          "type": "text",
          "text": {
            "value": "quero uma piada bem ruim sobre um pato amarelo",
            "annotations": []
          }
        }
      ],
      "object": "thread.message"
    },
    {
      "thread_id": "thread_CqbkLwvNZkyc3gv7YGOVDfHL",
      "metadata": {},
      "role": "user",
      "assistant_id": null,
      "run_id": null,
      "file_ids": [],
      "created_at": 1701683920,
      "id": "msg_pQ9owv948wTLlySg9yCoeH0V",
      "content": [
        {
          "type": "text",
          "text": {
            "value": "quero uma piada bem ruim sobre um pato amarelo",
            "annotations": []
          }
        }
      ],
      "object": "thread.message"
    },
    {
      "thread_id": "thread_CqbkLwvNZkyc3gv7YGOVDfHL",
      "metadata": {},
      "role": "user",
      "assistant_id": null,
      "run_id": null,
      "file_ids": [],
      "created_at": 1701683941,
      "id": "msg_XMJy8CLcbjHKI92dWb3NBQh7",
      "content": [
        {
          "type": "text",
          "text": {
            "value": "quero uma piada bem ruim sobre um pato amarelo",
            "annotations": []
          }
        }
      ],
      "object": "thread.message"
    },
    {
      "thread_id": "thread_CqbkLwvNZkyc3gv7YGOVDfHL",
      "metadata": {},
      "role": "user",
      "assistant_id": null,
      "run_id": null,
      "file_ids": [],
      "created_at": 1701684038,
      "id": "msg_S6Bd85LnDE5P0qefMbsz6wsl",
      "content": [
        {
          "type": "text",
          "text": {
            "value": "quero uma piada bem ruim sobre um pato amarelo",
            "annotations": []
          }
        }
      ],
      "object": "thread.message"
    },
    {
      "thread_id": "thread_CqbkLwvNZkyc3gv7YGOVDfHL",
      "metadata": {},
      "role": "user",
      "assistant_id": null,
      "run_id": null,
      "file_ids": [],
      "created_at": 1701684082,
      "id": "msg_pVFvPOkNoIX8K7ZIN3j7wjSc",
      "content": [
        {
          "type": "text",
          "text": {
            "value": "quero uma piada bem ruim sobre um pato amarelo",
            "annotations": []
          }
        }
      ],
      "object": "thread.message"
    }
  ],
  "telefone": "+5511983477360",
  "id": "thread_CqbkLwvNZkyc3gv7YGOVDfHL",
  "created": 1701682099,
  "status": "ativo"
}
```
# cliente
```
{
  "telefone": "+5511983477360",
  "nome": "Iphone+De+Teste+Fabiao",
  "modo_assistente": true,
  "created": "1701676465.966721"
}
```

# parametro
```
{
  "nome_gerente": "Alexandra Lucena",
  "modo_assistente": "ativo",
  "id": "1"
}
```
## 1 Como gerar o build
````
$ docker build -t fabioalvaro/poc-laranja:latest .
```````
# 2 como rodar a app

Crie um arquivo .env com as seguinte variaveis de ambiente

````
## Arquivo de configuracao /config/.env
AMBIENTE=PRODUCAO
GPT_API_KEY=sk-LEasdasdasdasd
ASSISTENTE_ID=asst_Z1pasdasdasd
BANCO=REMOTO
TWILIO_ACCOUNT=ACf1f1asdasdasd
TWILIO_AUTH_TOKEN=ecf987asdasdasd
TWILIO_BASIC_RESPOSTA=QUNmMWYasdasdasdasdasda
STATUS_CALLBACK=http://asdasdasd.compute-1.amazonaws.com:8080/poc-laranja/v1/service/health
REMETENTE_TWILIO_WHATS=186asdasdasdas
TWILIO_ACCOUNT_SID=ACf1f1f7asdasdasdasdas
VERSAO=V2

````

## gerando o docker
$ docker build -t fabioalvaro/poc-laranja:latest .
$ docker pull fabioalvaro/poc-laranja:latest

docker push fabioalvaro/poc-laranja:latest


$ docker run --name poc-laranja -v $PWD:/work -p 8080:8080 fabioalvaro/poc-laranja:latest 


### Diversos

pip freeze > requirements.txt
tmux attach -t flask
$ pip install flask_socketio

AMBIENTE=PRD
BANCO=REMOTO
VERSAO_LOGICA=V2
ASSISTENTE_ID_VAR=asst_Z1pMBbuDlAQLLJ0nyTMttgHl