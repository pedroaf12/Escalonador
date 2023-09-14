#Projeto Escalonador - Sistemas Operacionais 1

t_chegada = []
pico = []
qtd_process = 0

#----------------Abrindo o Arquivo---------------------------
arquivo = open("entradaTeste.txt")
for linha in arquivo:
    valores = linha.split()
    t_chegada.append(int(valores[0]))
    pico.append(int(valores[1]))
#print(t_chegada)
#print(pico)
arquivo.close()
qtd_process = len(t_chegada)


#---------------FCFS (First-Come, First-Served)----------------
processo = 0
t_decorrido = 0

t_espera_medio = 0
t_espera = []

t__retorno_medio = 0
t__retorno = []

t__resposta_medio = 0
t__resposta = []

t_restante_processo = []

for item in pico:
    t_restante_processo.append(item)

while True:
    
    if t_decorrido < t_chegada[processo]:
        t_decorrido += 1
        continue
    
    t_espera.insert(processo, t_decorrido - t_chegada[processo])
    t__resposta.insert(processo, t_decorrido - t_chegada[processo])

    while t_restante_processo[processo] > 0:
        t_restante_processo[processo] -= 1
        t_decorrido += 1
    else:
        t__retorno.insert(processo, t_decorrido - t_chegada[processo])
        processo += 1
    

    if processo == qtd_process :
        for soma in t_espera:
            t_espera_medio += soma
        for soma in t__retorno:
            t__retorno_medio += soma
        for soma in t__resposta:
            t__resposta_medio += soma

        t_espera_medio /= qtd_process
        t__retorno_medio /= qtd_process
        t__resposta_medio /= qtd_process
        break

#print(t_decorrido)
#print(t_espera)
#print(t_espera_medio)
#print(t__retorno)
#rint(t__retorno_medio)   
#print(t__resposta)
#print(t__resposta_medio)  
#---------------SJF (Shortest Job First)----------------
t_restante_processo.clear()

t_espera_medio = 0
t_espera.clear()

t__retorno_medio = 0 
t__retorno.clear()

t__resposta_medio = 0
t__resposta.clear()

processo = 0
t_decorrido = 0

for item in pico:
    t_restante_processo.append(item)
    
fila_prontos = []
fila_prontos_pico =[]

processo_pronto = 0
cont = 4
while cont > 0:
    
    
    while t_chegada[processo_pronto] == t_decorrido:
        fila_prontos.append(t_chegada[processo_pronto])
        fila_prontos_pico.append(pico[processo_pronto])
        processo_pronto += 1
    
    cont -= 1
    proximo_processo = min(fila_prontos_pico)
    proximo_procsso = fila_prontos_pico.index(proximo_processo)
    
    while t_restante_processo[proximo_processo] > 0:
        t_restante_processo[proximo_processo] -= 1
        t_decorrido += 1
    
else:
    print(fila_prontos)
    
    
    
    
        
    
    
