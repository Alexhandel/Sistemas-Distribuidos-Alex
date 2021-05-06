# Lab 4 servidor 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket
import select
import sys

HOST = ''
PORTA = 6003

#lista de I/O
entradas = [sys.stdin]
#conexoes ativas
conexoes = {}
estadoClientes={}
parClientes={}
usernames={}

#função que inicia o servidor e returna um socket
def iniciaServidor():
	# cria o socket 
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

	# vincula a localizacao do servidor
	mySocket.bind((HOST, PORTA))

	# coloca-se em modo de espera por conexoes
	mySocket.listen(5) 

	# configura o socket para o modo nao-bloqueante
	mySocket.setblocking(False)

	# inclui o socket principal na lista de entradas de interesse
	entradas.append(mySocket)

	return mySocket

def aceitaConexao(socket):
	'''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

	# estabelece conexao com o proximo cliente
	clienteSocket, endereco = socket.accept()

	# registra a nova conexao
	conexoes[clienteSocket] = endereco 
	estadoClientes[clienteSocket] = "menu"
	parClientes[clienteSocket] = ""
	usernames[clienteSocket] = " "


	return clienteSocket, endereco

def atendeRequisicoes(clienteSocket, endr):
	'''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
	Entrada: socket da conexao e endereco do cliente
	Saida: '''

	#recebe dados do cliente
	print("atendendendo requisisson")
	data = clienteSocket.recv(2048) 
	if not data: # dados vazios: cliente encerrou
		print(str(endr) + '-> encerrou')
		#retira o cliente das listas
		del conexoes[clienteSocket]
		del estadoClientes[clienteSocket]
		del parClientes[clienteSocket]
		del usernames[clienteSocket]
		entradas.remove(clienteSocket) #retira o socket do cliente das entradas do select
		clienteSocket.close() # encerra a conexao com o cliente
		return 

	#parte onde as coisas são feitas MUDE AQUI EM BAIXO
	#print(str(endr) + ': ' + str(data, encoding='utf-8'))
	#clienteSocket.send(data) # ecoa os dados para o cliente
	if estadoClientes[clienteSocket]=="menu":
		usernames[clienteSocket] = data.decode("utf-8")
		estadoClientes[clienteSocket] = "notMenu"
		clienteSocket.send(str.encode("nome mudado"))
		pass
	else:
		listaPalavras = []
		print("requisição para" + str(usernames[clienteSocket]))
		for name in usernames:
			listaPalavras.append(usernames[name])
		clienteSocket.send(str.encode(str(listaPalavras)))

def main():
	socket=iniciaServidor()
	print("Pronto para receber conexoes...")
	while True:
		#espera por qualquer entrada de interesse
		leitura, escrita, excecao = select.select(entradas, [], [])
		#tratar todas as entradas prontas
		for pronto in leitura:
			if pronto == socket:  #pedido novo de conexao
				clienteSocket, endr = aceitaConexao(socket)
				print ('Conectado com: ', endr)
				# configura o socket para o modo nao-bloqueante
				clienteSocket.setblocking(False)
				# inclui o socket principal na lista de entradas de interesse
				entradas.append(clienteSocket)
			elif pronto == sys.stdin: #entrada padrao
				cmd = input()
				if cmd == 'fim': #solicitacao de finalizacao do servidor
					if not conexoes: #somente termina quando nao houver clientes ativos
						socket.close()
						sys.exit()
					else: print("ha conexoes ativas")
				elif cmd == "lista":
					print("usuarios: ")
					for name in usernames:
						print(usernames[name])
			else: #nova requisicao de cliente
				atendeRequisicoes(pronto, conexoes[pronto])

main()