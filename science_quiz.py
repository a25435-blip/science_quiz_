import streamlit as st #para que o código funcione no site definido por nós
import os #O ficheiro "os" confirma que o ficheiro "Questoes.txt" existe, evitando que o programa dê erro e feche sozinho.

class Cores: #paleta de cores para deixar o código mais belo esteticamente
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    NEGRITO = '\033[1m'
    FIM = '\033[0m'


# --- GESTÃO DE DADOS ---

def carregar_perguntas(Questoes):
    perguntas = {} #Dicionário vazio para organizar as perguntas em cada tema, acumulando-as até que o programa feche
    if not os.path.exists(Questoes): #"os.path.exists" verifica se o ficheiro em conta (questoes) existe
        print(f"Erro: Ficheiro de perguntas não encontrado!{Cores.VERMELHO}{Questoes}{Cores.FIM}")
        return perguntas

    with open(Questoes, 'r', encoding='utf-8') as f:
        for linha in f:
            Tema, questao, a, b, c, correta = linha.strip().split(';') #".split(;)"Transforma uma string única numa lista, cortando-a sempre que encontrar o ";"
            if Tema not in perguntas:
                perguntas[Tema] = []
            perguntas[Tema].append({'Pergunta': questao,'opcoes': [a, b, c],'correta': correta})
    return perguntas


def guardar_pontuacao(nome, pontos):
    with open("ranking.txt", "a", encoding='utf-8') as f:
        f.write(f"{nome};{pontos}\n")


def exibir_ranking():
    print(f"\n{Cores.AZUL}--- RANKING GLOBAL ---{Cores.FIM}")
    if not os.path.exists("ranking.txt"): #"ranking.txt" é o ficheiro onde o nome e pontos dos jogadores saõ guardados
        print(f"{Cores.AMARELO}Ainda não há jogadores registados.{Cores.FIM}")
        return

    jogadores = []
    with open("ranking.txt", "r", encoding='utf-8') as f:
        for linha in f:
            nome, pontos = linha.strip().split(';')
            jogadores.append((nome, int(pontos)))

    # Ordena por pontuação (do maior para o menor)
    ranking_ordenado = sorted(jogadores, key=lambda x: x[1], reverse=True) #"reverse" é argumento da função sorted(), que inverte a ordem do ranking
   #"lambda" é uma função anónima que funciona como um argumento que "economiza código"
    for i, (nome, pontos) in enumerate(ranking_ordenado, 1): #O "enumerate" funciona como um organizador de listas/tuplas/dicionários que nos entrega pares como os indices e seus valores
        print(f"{i}º - {nome}: {pontos} pontos")


# --- LÓGICA DO JOGO ---

def jogar(perguntas_por_tema):
    print(f"{Cores.AMARELO}Bem-vindo ao Science Quiz!{Cores.FIM}")
    nome = st.text_input(f"{Cores.AMARELO}Introduza o seu nome: {Cores.FIM}")

    temas = list(perguntas_por_tema.keys())
    print(f"\n{Cores.NEGRITO}Temas disponíveis:{Cores.FIM}")
    for i, Tema in enumerate(temas, 1):
        print(f"{Cores.NEGRITO}{i}. {Tema}{Cores.FIM}")

    escolha = int(st.text_input("\nEscolha o número do tema: ")) - 1
    tema_escolhido = temas[escolha]

    pontuacao = 0
    questoes = perguntas_por_tema[tema_escolhido]

    for q in questoes:
        print(f"\n{q['Pergunta']}")
        opcoes_letras = ['A', 'B', 'C']
        for i, opcao in enumerate(q['opcoes']):
            print(f"{opcoes_letras[i]}) {opcao}")
        resposta = st.text_input("Qual a sua resposta (A, B, ou C)? ").upper().lower()#".lower()" transforma "A" em "a" e o "upper()" transforma "a" em "A"
        if resposta == q['correta']:
           print(f"{Cores.VERDE}Correto! (+20 pontos){Cores.FIM}")
           pontuacao += 20
        else:
            print(f"{Cores.VERMELHO}Errado! A resposta correta era {q['correta']}{Cores.FIM}.")

    print(f"{Cores.AMARELO}\nFim de jogo, {nome}! Pontuação Final: {pontuacao}/100{Cores.FIM}")
    guardar_pontuacao(nome, pontuacao)


# --- EXECUÇÃO PRINCIPAL ---

banco_perguntas = carregar_perguntas("Questoes.txt")

if banco_perguntas:
    jogar(banco_perguntas)
    exibir_ranking()
