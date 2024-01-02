import redis

# Precisamos da configuração padrão do nosso pianista Redis
redis_host = "localhost"
redis_port = 6379
redis_password = ""  # Substitua se o seu Redis estiver com senha

# Vamos fazer a conexão com o Redis
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Agora, a parte emocionante: armazenar a linha no Redis
chave = "minha_chave"
valor = "Olá, Redis!"

try:
	# Executamos a partitura da inserção
    resultado = r.set(chave, valor)
    if resultado:
        print(f"Linha gravada com sucesso! Chave: {chave}, Valor: {valor}")
    else:
        print("Falha ao gravar a linha no Redis.")
except Exception as e:
    # Nosso salvaguarda contra notas desafinadas
    print(f"Erro ao gravar no Redis: {e}")