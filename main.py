
import os
import requests

response = requests.get("https://random-word-api.herokuapp.com/word?number=1&diff=1&lang=pt-br")
palavra_secreta =  response.json()[0]
letras_acertadas = ''
numero_tentativas = 0
limite_de_tentativas = len(palavra_secreta) 
while True:
    if limite_de_tentativas <= 0:
        print('acabaram as tentativas')
        print('A palavra era ', palavra_secreta)
        break     
    letra_digitada = input('Digite uma letra: ')
    numero_tentativas += 1
    limite_de_tentativas -= 1
    if len(letra_digitada) > 1:
        print('Digite apenas uma letra.')
        continue

    if letra_digitada in palavra_secreta:
        letras_acertadas += letra_digitada

    palavra_formada = ''
    for letra_secreta in palavra_secreta:
        if letra_secreta in letras_acertadas:
            palavra_formada += letra_secreta
        else:
            palavra_formada += '*'

    print('Palavra formada:', palavra_formada)
    print("Tentativas restantes: ", limite_de_tentativas)
    if palavra_formada == palavra_secreta:
        os.system('clear')
        print('VOCÊ GANHOU!! PARABÉNS!')
        print('A palavra era', palavra_secreta)
        print('Tentativas:', numero_tentativas)
        print('Tentativas restantes:', limite_de_tentativas)
        letras_acertadas = ''
        numero_tentativas = 0
        limite_de_tentativas = 0
   
