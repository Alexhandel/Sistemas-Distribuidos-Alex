# Lab 4 servidor 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket
import select
import sys
import threading

HOST = ''
PORTA = 6004

#lista de I/O
entradas = [sys.stdin]
#conexoes ativas
conexoes = {}
estadoClientes={}
parClientes={}
usernames={}
#lock
lock = threading.Lock()

#função que inicia o servidor e returna um socket
def iniciaServidor():
	# cria o socket 
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 
	mySocket.bind((HOST, PORTA))
	mySocket.listen(5) 
	mySocket.setblocking(False)
	entradas.append(mySocket)

	return mySocket

#função que estabelece conexão com socket cliente e retorna o socket do cliente e seu endereco
def aceitaConexao(socket):
	# estabelece conexao com o proximo cliente
	clienteSocket, endereco = socket.accept()

	# registra a nova conexao
	lock.acquire()
	conexoes[clienteSocket] = endereco 
	estadoClientes[clienteSocket] = "start"
	parClientes[clienteSocket] = ""
	usernames[clienteSocket] = " "
	lock.release()


	return clienteSocket, endereco

#função principal que processa todas mensagens de um unico cliente
#cada iteração do loop dessa função deverá ter um unico receive e um unico send
def processaRequisicoes(clienteSocket, endr):

	while True:
		#pega mensagem
		data = clienteSocket.recv(2048) 
		msg = data.decode("utf-8")
		if not data: # dados vazios: cliente encerrou
			print(str(endr) + '-> encerrou')
			lock.acquire()
			del conexoes[clienteSocket]
			del estadoClientes[clienteSocket]
			del parClientes[clienteSocket]
			del usernames[clienteSocket]
			lock.release()
			clienteSocket.close()
			return 

		#faz coisas diferentes dependendo do estado do cliente	
		if estadoClientes[clienteSocket]=="start": #cliente começa aqui, define nome de usuario
			usernameTaken=False
			#checa nome de usuario invalido
			if msg[0:2]=="--":
				clienteSocket.send(str.encode(">nome de usuario não pode começar com '--' por favor escolha outro"))
			else:
				#checa se o nome de usuario está em uso
				if len(usernames) > 0:
					for user in usernames:
						if msg==usernames[user]:
							usernameTaken=True
				#muda o nome de usuario caso esteja disponivel
				if usernameTaken==False:
					lock.acquire()
					usernames[clienteSocket] = msg
					estadoClientes[clienteSocket] = "menu"
					lock.release()
					clienteSocket.send(str.encode(">nome definido, voce está no menu agora. Comandos são 'lista' para ver usuarios conectados e 'conectar' para mandar mensagens"))
				else:
					clienteSocket.send(str.encode(">nome em uso por favor escolha outro"))
		#parte que faz coisa do menu
		#menu tem 2 comandos: conectar e lista
		elif estadoClientes[clienteSocket]=="menu":
			#comando para conectar com outro usuario e começar troca de mensagem
			if msg == "conectar":
				lock.acquire()
				estadoClientes[clienteSocket]="conectando"
				lock.release()
				clienteSocket.send(str.encode("digite o nome do usuario que deseja conectar ou '--sair' para voltar ao menu"))
			#comando para mostar lista de usuarios conectados
			elif msg == "lista":
				listaPalavras = []
				for name in usernames:
					listaPalavras.append(usernames[name])
				clienteSocket.send(str.encode(str(listaPalavras)))
			#nada acontece em caso de comando desconhecido
			else:
				clienteSocket.send(str.encode(" "))
		#parte que pergunta a qual outro usuario o cliente quer mandar mensagem e faz a conexão
		elif estadoClientes[clienteSocket]=="conectando":
			if msg == "--sair": #permite voltar ao menu sem fazer conexão
				lock.acquire()
				estadoClientes[clienteSocket]="menu"
				lock.release()
				clienteSocket.send(str.encode("retornado ao menu"))
			#caso não encontre o usuario requerido
			elif msg not in usernames.values(): 
					clienteSocket.send(str.encode("nome de usuario não encontrado, digite outro"))
			# faz a conexão
			else: 
				lock.acquire()
				parClientes[clienteSocket]=msg
				estadoClientes[clienteSocket]="mensagem"
				lock.release()
				clienteSocket.send(str.encode("agora mandando mensagens para " + msg + ", digite '--menu' para voltar ao menu"))
		#parte que manda mensagem a outro usuario
		elif estadoClientes[clienteSocket]=="mensagem":
			if msg != "--menu": 
				nomePar=parClientes[clienteSocket]
				if nomePar not in usernames.values(): #retorna ao menu caso o usuario esteja desconectado
					lock.acquire()
					estadoClientes[clienteSocket]="menu"
					lock.release()
					clienteSocket.send(str.encode("usuario foi desconectado, voltando ao menu"))
					continue
				for key,values in usernames.items(): #busca o nome na lista
					if values==nomePar:
						par=key
				par.send(str.encode("mensagem de [" + str(usernames[clienteSocket]) + "]: " + msg))
			#voltar a menu
			else:
				lock.acquire()
				estadoClientes[clienteSocket]="menu"
				lock.release()
				clienteSocket.send(str.encode("retornado ao menu"))
			
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
				cliente = threading.Thread(target=processaRequisicoes, args=(clienteSocket,endr))
				cliente.start()
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

main()