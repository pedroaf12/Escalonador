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




while True:
    t_espera.insert(processo, t_decorrido - t_chegada[processo])
    t__resposta.insert(processo, t_decorrido - t_chegada[processo])

    while pico[processo] > 0:
        pico[processo] -= 1
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

print(t_decorrido)
print(t_espera)
print(t_espera_medio)
print(t__retorno)
print(t__retorno_medio)   
print(t__resposta)
print(t__resposta_medio)  
#---------------SJF (Shortest Job First)----------------