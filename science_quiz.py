import streamlit as st #Para funcionar no site (python de web)
import os #O ficheiro "os" confirma que o ficheiro "Questoes.txt" existe, evitando que o programa dê erro e feche sozinho

class Cores: 
    VERDE = ''
    AMARELO = ''
    VERMELHO = ''
    AZUL = ''
    NEGRITO = ''
    FIM = ''

# --- GESTÃO DE DADOS ---

def carregar_perguntas(Questoes):
    perguntas = {} 
    if not os.path.exists(Questoes):
        st.error(f"Erro: Ficheiro de perguntas não encontrado! {Questoes}")
        return perguntas

    with open(Questoes, 'r', encoding='utf-8') as f:
        for linha in f:
            if ";" in linha:
                Tema, questao, a, b, c, correta = linha.strip().split(';')
                if Tema not in perguntas:
                    perguntas[Tema] = []
                perguntas[Tema].append({'Pergunta': questao,'opcoes': [a, b, c],'correta': correta})
    return perguntas

def guardar_pontuacao(nome, pontos):
    with open("ranking.txt", "a", encoding='utf-8') as f:
        f.write(f"{nome};{pontos}\n")

def exibir_ranking():
    st.subheader("--- RANKING GLOBAL ---")
    if not os.path.exists("ranking.txt"):
        st.write("Ainda não há jogadores registados.")
        return

    jogadores = []
    with open("ranking.txt", "r", encoding='utf-8') as f:
        for linha in f:
            if ";" in linha:
                nome, pontos = linha.strip().split(';')
                jogadores.append((nome, int(pontos)))

    ranking_ordenado = sorted(jogadores, key=lambda x: x[1], reverse=True)
    for i, (nome, pontos) in enumerate(ranking_ordenado, 1):
        st.write(f"{i}º - {nome}: {pontos} pontos")

# --- LÓGICA DO JOGO ---

def jogar(perguntas_por_tema):
    st.title("🚀 Science Quiz")
    
    nome = st.text_input("Introduza o seu nome:")
    if not nome:
        st.warning("Por favor, introduza o seu nome para começar.")
        st.stop()

    temas = list(perguntas_por_tema.keys())
    st.write("### Temas disponíveis:")
    for i, Tema in enumerate(temas, 1):
        st.write(f"{i}. {Tema}")

    escolha_input = st.text_input("Escolha o número do tema (ex: 1):")
    
    if escolha_input: 
        try:
            indice = int(escolha_input) - 1
            tema_escolhido = temas[indice]
        except:
            st.error("Por favor, insira um número válido.")
            st.stop()
            
        pontuacao = 0
        questoes = perguntas_por_tema[tema_escolhido]

        for idx, q in enumerate(questoes):
            st.markdown(f"---")
            st.write(f"**{q['Pergunta']}**")
            
            # Usar selectbox ou radio para as respostas no Streamlit funciona melhor que text_input
            opcoes = [f"A) {q['opcoes'][0]}", f"B) {q['opcoes'][1]}", f"C) {q['opcoes'][2]}"]
            resposta_user = st.radio(f"Escolha a sua resposta para a questão {idx+1}:", ["-"] + opcoes, key=f"quest_{idx}")

            if resposta_user != "-":
                letra_escolhida = resposta_user[0] # Pega apenas o 'A', 'B' ou 'C'
                if letra_escolhida.lower() == q['correta'].lower():
                    st.success("Correto! (+20 pontos)")
                    pontuacao += 20
                else:
                    st.error(f"Errado! A resposta correta era {q['correta']}.")

        if st.button("Finalizar e Guardar Pontuação"):
            st.balloons()
            st.info(f"Fim de jogo, {nome}! Pontuação Final: {pontuacao}")
            guardar_pontuacao(nome, pontuacao)
            st.session_state['ver_ranking'] = True

# --- EXECUÇÃO PRINCIPAL ---

banco_perguntas = carregar_perguntas("Questoes.txt")

if banco_perguntas:
    jogar(banco_perguntas)
    if st.session_state.get('ver_ranking'):
        exibir_ranking()
