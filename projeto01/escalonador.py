#Projeto Escalonador - Sistemas Operacionais 1

QUANTUM = 2               #tempo maximo de execução por vez no RR
t_chegada = []            #tempo de chegada dos processos na fila de prontos
pico = []                 #Tempo que cada processo precisa dentro da cpu para executar
qtd_process = 0           #quantidade de processos que vão ser executados na cpu


t_espera_medio = 0        
t_espera = []

t_retorno_medio = 0
t_retorno = []

t_resposta_medio = 0
t_resposta = []

t_restante_processo = []  #Lista com o tempo que falta para cada processo terminar sua execução

#------------------------------Abrindo o Arquivo-------------------------------
arquivo = open("entradaTeste.txt")
for linha in arquivo:
    valores = linha.split()
    t_chegada.append(int(valores[0]))
    pico.append(int(valores[1]))
arquivo.close()
qtd_process = len(t_chegada)


#------------------------------Calcula média dos tempos----------------------------

#Recebe as listas com os tempos de espera, retorno e resposta de todos
#os processos e soma e divide pela quantidade de processos executados
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
    
    return t_retorno_medio, t_resposta_medio, t_espera_medio

#----------------------Limpar as listas com os tempos dos processos--------------------

def limpar_valores():
    t_restante_processo.clear()
    t_espera.clear()
    t_retorno.clear()
    t_resposta.clear()
    
#---------------------------FCFS (First-Come, First-Served)-----------------------
def fcfs():
    processo = 0           #Processo atual que vai entrar na cpu
    t_decorrido = 0        #Simula quantas unidades de tempo já se passarem

    #Iniciando a lista de tempo restando com a lista de pico(tempo necessario de cpu para executar)
    for item in pico:
        t_restante_processo.append(item)

    
    while True:
        
        #Conta uma unidade de tempo caso ainda não tenha chegado algum processo na "fila de pronto"
        if t_decorrido < t_chegada[processo]:
            t_decorrido += 1
            continue
        
        #Por ser FCFS e o processo uma vez dentro da cpu, só sai quando terminar execução
        #Tempo de espera e resposta são calculados juntos
        #Antes de cada processo entrar na cpu esses tempos são calculados
        t_espera.insert(processo, t_decorrido - t_chegada[processo])
        t_resposta.insert(processo, t_decorrido - t_chegada[processo])

        #Simula uma cpu executando uma unidade de tempo do processo por vez
        while t_restante_processo[processo] > 0:   #Processo sai quando termina totalmente sua execução
            t_restante_processo[processo] -= 1     #Simula a execução do processo
            t_decorrido += 1                       #Simula a passagem de tempo 
        #Ao final da execução calcula o tempo de retorno do processo
        else:
            t_retorno.insert(processo, t_decorrido - t_chegada[processo])
            processo += 1   #Da a vez para o proximo processo que chegar
        
        #Indica que não vai chegar mais processos
        #então pode calcular a media dos tempos
        if processo == qtd_process :
            valor_final = calcula_media(t_retorno=t_retorno, t_resposta=t_resposta, t_espera=t_espera)
            break

    print('FCFS {:.1f} {:.1f} {:.1f}'.format(valor_final[0], valor_final[1], valor_final[2]))
#-------------------------SJF (Shortest Job First)---------------------------
def sjf():
    limpar_valores()        #Limpa as listas dos tempos

    processo = 0             #Processo atual 
    t_decorrido = 0

    for item in pico:
        t_restante_processo.append(item)
    
    #Representação da fila de prontos no SFJ
    index_processo = []       #Index dos processos na lista t_restante_processo 
    fila_prontos =[]          #Lista com o pico dos processos que chegaram até o momento

    processo_pronto = 0       #Indica o processo que acabou de chegar na lista de prontos
                              #Indica quantos processos já chegaram na lista de prontos(quantidade)

    while True:
        
        #Verifica se algum processo chegou até o momento para colocar na fila de prontos
        while processo_pronto < qtd_process and t_chegada[processo_pronto] <= t_decorrido:
            fila_prontos.append(pico[processo_pronto])
            index_processo.append(processo_pronto)
            processo_pronto += 1
            
        #Se nenhum processo chegou, passa então uma unidade de tempo sem a cpu fazer nada
        if len(fila_prontos) == 0:
            t_decorrido += 1
            continue   

        #Sendo SJF procura o processo com menor tempo necessario
        proximo_processo = min(fila_prontos)
        #Descoble o index dele na fila de prontos para cruzar com o index na lista de index de t_restante_processo
        processo = fila_prontos.index(proximo_processo)
        #Sabendo que após selecionado não vi mais voltar para fila de prontos
        #É removido da fila de prontos
        fila_prontos.remove(proximo_processo)
        #Indica qual o processe será executado enfim na cpu
        processo = index_processo[processo]

        #Por ser SJF e o processo uma vez dentro da cpu, só sai quando terminar execução
        #Tempo de espera e resposta são calculados juntos
        #Antes de cada processo entrar na cpu esses tempos são calculados
        t_espera.insert(processo, t_decorrido - t_chegada[processo])
        t_resposta.insert(processo, t_decorrido - t_chegada[processo])
        
        #Simula uma cpu executando uma unidade de tempo do processo por vez
        while t_restante_processo[processo] > 0:   #Processo sai quando termina totalmente sua execução
            t_restante_processo[processo] -= 1     #Simula a execução do processo
            t_decorrido += 1                       #Simula a passagem de tempo 
        #Ao final da execução calcula o tempo de retorno do processo
        else:
            t_retorno.insert(processo, t_decorrido - t_chegada[processo])
            index_processo.remove(processo)
        
        #Verifica se o ultimo processo executou
        #então calcula a media do tempos
        if processo_pronto >= qtd_process and len(fila_prontos) == 0:
            valor_final = calcula_media(t_retorno=t_retorno, t_resposta=t_resposta, t_espera=t_espera)
            break

    print('FJS {:.1f} {:.1f} {:.1f}'.format(valor_final[0], valor_final[1], valor_final[2])) 

#-------------------------RR2 (Shortest Job First)---------------------------
def rr2():  
    limpar_valores()

    processo = 0        #Processo atual 
    t_decorrido = 0

    for item in pico:
        t_restante_processo.append(item)


    index_processo = []
    fila_prontos =[]
    
    saida_cpu = []      #Guarda o momento que o processo sai da cpu

    #Inicializa a lista saida_cpu com t_chegada
    #Já que o tempo de chegada vai ser usado no calculo do tempo de espera
    #quando o processo entra pela primeira vez na cpu t_decorrido - saida_cpu
    for item in t_chegada:
        saida_cpu.append(item)

    proximo_processo = 0    #Zera para não ter problema de sincronização antesd e entrar
    processo_pronto = 0
    execucao = 0            #Quantas vezes o processo executou na cpu dps que entrou

    finalizados = 0         #Quantos processos ja terminaram
        
    while True:
        
        #Verifica se algum processo chegou até o momento para colocar na fila de prontos
        while processo_pronto < qtd_process and t_chegada[processo_pronto] <= t_decorrido:
            fila_prontos.append(pico[processo_pronto])
            index_processo.append(processo_pronto)
            processo_pronto += 1
        
        #Se nenhum processo chegou, passa então uma unidade de tempo sem a cpu fazer nada
        if len(fila_prontos) == 0:
            t_decorrido += 1
            continue  

        #indica o processo que vai entrar na cpu
        processo = index_processo[proximo_processo]
        
        #Verifica se é a primeira vez do processo entrando na cpu
        #Se sim, calcula o tempo de resposta
        if fila_prontos[processo] > 0:
            t_resposta.insert(processo, t_decorrido - t_chegada[processo])
            fila_prontos[processo] = 0
            #Inicializa o tempo de espera desse processo para fins de calculo
            #Já que a partir desse momento seu tempo de espera sera contado
            t_espera.insert(processo, 0)

        #Se o processo ainda não tiver terminado calcula o tempo total que ficou
        #na fila de prontos sem executar até o momento
        if t_restante_processo[processo] > 0:
            t_espera[processo] += t_decorrido - saida_cpu[processo]

        #Simula a cpu
        #executa no maximo duas unidades de tempo a cada processo que entra
        while t_restante_processo[processo] > 0 and execucao < QUANTUM:
            t_restante_processo[processo] -= 1
            t_decorrido += 1
            execucao += 1 
            saida_cpu[processo] = t_decorrido

            #Verifica se o processo finalizou
            #Se sim, calcula seu tempo de retorno
            if t_restante_processo[processo] == 0:
                t_retorno.insert(processo, t_decorrido - t_chegada[processo])
                finalizados += 1    #Indica que mais um processo terminou completamente
            
        else:
            #Apos cada ciclo de quamtum na cpu, verifica se sechou mais algum processo
            while processo_pronto < qtd_process and t_chegada[processo_pronto] <= t_decorrido:
                fila_prontos.append(pico[processo_pronto])
                index_processo.append(processo_pronto)
                processo_pronto += 1

            #Troca a posição do processo que abou de execuar com o ultimo da lista de prontos
            #Para o RR da lista de prontos só necessito saber os index deles na lista de tempo restante
            aux = index_processo[proximo_processo]
            index_processo[proximo_processo] = index_processo[len(index_processo) -1]
            index_processo[len(index_processo) -1] = aux

            #libera para a cpu executar mais QUANTUM unidade de tempo
            execucao = 0
            
            #Verifica se caso o unico processo na fila de prontos ja terminou
            #Uma unidade de tempo vai se passar sem a cpu ter algo para executar
            if len(fila_prontos) == 1 and t_restante_processo[processo] == 0:
                t_decorrido += 1
                continue
            
            #então tem o que ser executado
            #indica o proximo a ser executado
            proximo_processo += 1
            
        #Caso o proximo processo a ser executado sera o unico na lista
        #configura para não avançar o contador de processo
        if proximo_processo == len(index_processo) - 1 or len(fila_prontos) == 1:
                proximo_processo = 0   
        
        #Verifica se todos os processos terminaram
        #Calcula a media dos tempos
        if finalizados == qtd_process:
            valor_final = calcula_media(t_retorno=t_retorno, t_resposta=t_resposta, t_espera=t_espera)
            break
        
    print('RR2 {:.1f} {:.1f} {:.1f}'.format(valor_final[0], valor_final[1], valor_final[2]))

fcfs()
sjf()
rr2()
    
