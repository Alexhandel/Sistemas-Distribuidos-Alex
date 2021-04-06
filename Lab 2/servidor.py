import socket
import re

HOST = ''
PORTA = 6001

#inicializa o socket e coloca em modo de espera
sock = socket.socket() 
sock.bind((HOST, PORTA))
sock.listen(1) 

#aceita conexão
novoSock, endereco = sock.accept()
print ('Conectado com: ', endereco)

#loop que recebe mensagem e manda de volta
while True:
	msg = novoSock.recv(2048)
	nomeArquivo=str(msg, encoding='utf-8')

	#camada de acesso

	try: #try para o open() 
		arquivo=open(nomeArquivo, "r", encoding="utf8")
		novoSock.send(str.encode("fileFound"))
	except IOError: #exceção caso o arquivo não seja encontrado
		msg=str.encode("arquivo não encontrado")
		novoSock.send(msg)
		continue

	#camada de processamento

	#guarda o texto do arquivo em string na variavel
	textoArquivo=arquivo.read()
	#lista de todas as palavras no arquivo (regex tira caracteres não-alfanumericos)
	listaPalavras = re.split('[^a-zA-Z0-9\u00C0-\u00FF]', textoArquivo)
	#dict das palavras no arquivo, com duplicatas removidas.
	dictPalavras = dict.fromkeys(listaPalavras)
	
	#loop que conta a frequancia de cada palavra
	for key in dictPalavras: 
		dictPalavras[key]=listaPalavras.count(key)
	
	#faz um sort no dict por valor
	dictPalavras={k: v for k, v in sorted(dictPalavras.items(), key=lambda item: item[1], reverse=True)}
	#faz lista das 10 palavras com mais frequencia e lista das frequencias
	# o primeiro valor é descartado por ser espaço
	listaOrdenadaPalavras=list(dictPalavras.keys())[1:11]
	listaOrdenadaFrequencias=list(dictPalavras.values())[1:11]
	#faz duas string das listas e manda as duas
	p=str(listaOrdenadaPalavras)
	f=str(listaOrdenadaFrequencias)
	novoSock.send(str.encode(p))
	novoSock.send(str.encode(f))	

#fecha
novoSock.close() 
sock.close() 
