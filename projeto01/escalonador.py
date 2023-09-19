#Projeto Escalonador - Sistemas Operacionais 1

t_chegada = []
pico = []
qtd_process = 0
QUANTUM = 2

#------------------------------Abrindo o Arquivo-------------------------------
arquivo = open("entradaTeste.txt")
for linha in arquivo:
    valores = linha.split()
    t_chegada.append(int(valores[0]))
    pico.append(int(valores[1]))
#print(t_chegada)
#print(pico)
arquivo.close()
qtd_process = len(t_chegada)

def calcula_media(t_espera, t_retorno, t_resposta):

    t_espera_medio = 0
    t_retorno_medio = 0
    t_resposta_medio = 0
    
    for soma in t_espera:
        t_espera_medio += soma
    for soma in t_retorno:
        t_retorno_medio += soma
    for soma in t_resposta:
        t_resposta_medio += soma

    t_espera_medio /= qtd_process
    t_retorno_medio /= qtd_process
    t_resposta_medio /= qtd_process

    print("ACABOU")
    print("retorno")
    print(t_retorno)
    print(t_retorno_medio)
    print("resposta")
    print(t_resposta)
    print(t_resposta_medio)
    print("espera")
    print(t_espera)
    print(t_espera_medio)
        

#---------------------------FCFS (First-Come, First-Served)-----------------------
processo = 0
t_decorrido = 0

t_espera_medio = 0
t_espera = []

t_retorno_medio = 0
t_retorno = []

t_resposta_medio = 0
t_resposta = []

t_restante_processo = []

for item in pico:
    t_restante_processo.append(item)

while True:
    
    if t_decorrido < t_chegada[processo]:
        t_decorrido += 1
        continue
    
    t_espera.insert(processo, t_decorrido - t_chegada[processo])
    t_resposta.insert(processo, t_decorrido - t_chegada[processo])

    while t_restante_processo[processo] > 0:
        t_restante_processo[processo] -= 1
        t_decorrido += 1
    else:
        t_retorno.insert(processo, t_decorrido - t_chegada[processo])
        processo += 1
    

    if processo == qtd_process :
        calcula_media(t_retorno=t_retorno, t_resposta=t_resposta, t_espera=t_espera)
        break


#-------------------------SJF (Shortest Job First)---------------------------
t_restante_processo.clear()

#t_espera_medio = 0
t_espera.clear()

#t_retorno_medio = 0 
t_retorno.clear()

#t_resposta_medio = 0
t_resposta.clear()

processo = 0
t_decorrido = 0

for item in pico:
    t_restante_processo.append(item)
    
index_processo = []
fila_prontos =[]

processo_pronto = 0

cont = 0  #Contador de quantos processos ja estão na fila de prontos
          #Posso so usar o processo_pronto

while True:
    
    
    while cont < qtd_process and t_chegada[processo_pronto] <= t_decorrido:
        fila_prontos.append(pico[processo_pronto])
        index_processo.append(processo_pronto)
        processo_pronto += 1
        cont += 1
        

    if len(fila_prontos) == 0:
        t_decorrido += 1
        continue   

    #print(t_restante_processo)
    #print(fila_prontos)
    #print(index_processo)

    proximo_processo = min(fila_prontos)
    processo = fila_prontos.index(proximo_processo)
    fila_prontos.remove(proximo_processo)
    processo = index_processo[processo]

    t_espera.insert(processo, t_decorrido - t_chegada[processo])
    t_resposta.insert(processo, t_decorrido - t_chegada[processo])
    
    while t_restante_processo[processo] > 0:
        t_restante_processo[processo] -= 1
        t_decorrido += 1
        #print(t_restante_processo)
    else:
        t_retorno.insert(processo, t_decorrido - t_chegada[processo])
        index_processo.remove(processo)
    
    if cont >= qtd_process and len(fila_prontos) == 0:
        calcula_media(t_retorno=t_retorno, t_resposta=t_resposta, t_espera=t_espera)
        break

    
    #print(cont)
    #print(processo_pronto)
    



 #-------------------------RR2 (Shortest Job First)---------------------------  
t_restante_processo.clear()

t_espera_medio = 0
t_espera.clear()

t_retorno_medio = 0 
t_retorno.clear()

t_resposta_medio = 0
t_resposta.clear()

processo = 0        #Processo atual 
t_decorrido = 0


for item in pico:
    t_restante_processo.append(item)


index_processo = []
fila_prontos =[]
saida_cpu = []

for item in t_chegada:
    saida_cpu.append(item)

proximo_processo = 0
processo_pronto = 0
execucao = 0

cont = 0
    
while True:
    
    while processo_pronto < qtd_process and t_chegada[processo_pronto] <= t_decorrido:
        fila_prontos.append(pico[processo_pronto])
        index_processo.append(processo_pronto)
        processo_pronto += 1
    
    
    if len(fila_prontos) == 0:
        t_decorrido += 1
        continue  

    
    processo = index_processo[proximo_processo]
    

    if fila_prontos[processo] > 0:
        t_resposta.insert(processo, t_decorrido - t_chegada[processo])
        fila_prontos[processo] = 0
        t_espera.insert(processo, 0)

    if t_restante_processo[processo] > 0:
        t_espera[processo] += t_decorrido - saida_cpu[processo]
        #print(t_espera)

    while t_restante_processo[processo] > 0 and execucao < QUANTUM:
        t_restante_processo[processo] -= 1
        t_decorrido += 1
        execucao += 1
        saida_cpu[processo] = t_decorrido

        if t_restante_processo[processo] == 0:
            t_retorno.insert(processo, t_decorrido - t_chegada[processo])
            cont += 1
        
    else:
        while processo_pronto < qtd_process and t_chegada[processo_pronto] <= t_decorrido:
            fila_prontos.append(pico[processo_pronto])
            index_processo.append(processo_pronto)
            processo_pronto += 1

        aux = index_processo[proximo_processo]
        index_processo[proximo_processo] = index_processo[len(index_processo) -1]
        index_processo[len(index_processo) -1] = aux

        execucao = 0
        
        if len(fila_prontos) == 1 and t_restante_processo[processo] == 0:
            t_decorrido += 1
            continue
        
        proximo_processo += 1
        
        
    if proximo_processo == len(index_processo) - 1 or len(fila_prontos) == 1:
            proximo_processo = 0   
    
    if cont == qtd_process:
        calcula_media(t_retorno=t_retorno, t_resposta=t_resposta, t_espera=t_espera)
        break
        
print(t_resposta_medio)


    
    
