import os
import requests
import sqlite3
from datetime import datetime

# ---------------- BANCO ---------------- #

def conectar():
    return sqlite3.connect('dicionario.db')  # tirei o acento (evita erro)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS palavras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palavra TEXT,
            data_criacao TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def salvar_palavras(palavra):
    conn = conectar()
    cursor = conn.cursor()
    
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO palavras (palavra, data_criacao)
        VALUES (?, ?)
    ''', (palavra, data))
    
    conn.commit()
    conn.close()

# cria tabela ao iniciar
criar_tabela()

# ---------------- JOGO ---------------- #

palavra_secreta = None

print("Buscando palavra adequada...")

while not palavra_secreta:
    try:
        # Pede 10 palavras aleatórias à API
        response = requests.get("https://random-word-api.herokuapp.com/word?number=10&lang=pt-br")
        
        if response.status_code == 200:
            lista_palavras = response.json()
            
            # Percorre a lista de 10 palavras recebidas
            for p in lista_palavras:
                if len(p) <= 6:
                    palavra_secreta = p
                    break # Encontrou uma, sai do loop 'for'
            
            # Se após o 'for' palavra_secreta ainda for None, 
            # o 'while' rodará novamente para buscar mais 10.
            
    except Exception as e:
        print(f"Erro na conexão: {e}")
        continue
      


# salva no banco
salvar_palavras(palavra_secreta)

letras_acertadas = ''
numero_tentativas = 0
limite_de_tentativas = len(palavra_secreta)

while True:
    if limite_de_tentativas <= 0:
        print('Acabaram as tentativas!')
        print('A palavra era:', palavra_secreta)
        break

    letra_digitada = input('Digite uma letra: ').lower()

    if len(letra_digitada) != 1:
        print('Digite apenas UMA letra.')
        continue

    numero_tentativas += 1
    limite_de_tentativas -= 1

    if letra_digitada in palavra_secreta:
        letras_acertadas += letra_digitada

    palavra_formada = ''
    for letra in palavra_secreta:
        if letra in letras_acertadas:
            palavra_formada += letra
        else:
            palavra_formada += '*'

    # limpar tela (compatível)
    os.system('cls' if os.name == 'nt' else 'clear')

    print('Palavra:', palavra_formada)
    print('Tentativas restantes:', limite_de_tentativas)

    if palavra_formada == palavra_secreta:
        print('\n🎉 VOCÊ GANHOU!')
        print('Palavra:', palavra_secreta)
        print('Tentativas:', numero_tentativas)
        break