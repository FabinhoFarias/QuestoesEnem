import streamlit as st
import requests
from PaginaDeListas import pooo

def RequestTextoQuestao(ANO, NUMERO):
    Questao = requests.request("GET", f"https://api.enem.dev/v1/exams/{ANO}/questions/{NUMERO}").json()
    return Questao

    # st.html(f"{Questao["discipline"]} -- {Questao["title"]}") COLOCAR EM OUTRA FUNCAO PARA PRINTAR OS COMPONENTES

def QuebraComponentesQuestao(QuestaoJson, TextoQuestao, contador):
    DOMINIO = "https://api.enem.dev"
    ListaComponentesQuestao = []
    if DOMINIO not in TextoQuestao: # Caso base
        ListaComponentesQuestao.append(TextoQuestao)
        return ListaComponentesQuestao
    else:
        ListaPivo = TextoQuestao.split(f"![]({QuestaoJson["files"][contador]})")
        ListaComponentesQuestao.append(ListaPivo[0])
        ListaComponentesQuestao.append(QuestaoJson["files"][contador])
        contador += 1
        if ListaPivo[-1]:
            return QuebraComponentesQuestao(QuestaoJson, ListaPivo[-1], contador)

def ImprimirQuestao(QUESTAO, ListaComponentesQuestao, DOMINIO):
    for Componente in ListaComponentesQuestao:
        if DOMINIO in Componente:
            st.image(Componente, caption="Imagem da Questão")
        else:
            st.write(Componente)
    st.markdown("---")
    st.write(f"**{QUESTAO['alternativesIntroduction']}**") # https://api.enem.dev/v1/exams/2011/questions/141 fazer gambiarra depois para poder evitar questoes incompletas como essa
    for Alternativa in QUESTAO["alternatives"]:
        # crio botão
        st.markdown("---")
        if Alternativa["text"]: #Se houver texto
            if st.button(f"{Alternativa['letter']}: {Alternativa['text']}"):
                if Alternativa["isCorrect"]:
                    st.write(f"Alternativa CORRETA :)")
        else: # há imagem
            st.image(Alternativa["file"], caption="Alternativa")
            if Alternativa["isCorrect"]:
                st.write(f"Alternativa ERRADA :(")
    st.markdown("---")
   




def main():
    if "page" not in st.session_state:
        st.session_state.page = "PaginaInicial"

    if st.session_state.page == "PaginaInicial":
        st.title("Procure a questão que você deseja !")
        
    AnoQuestao    = int(st.slider("Digite o Ano da Prova:", min_value=2009, max_value=2023))    
    NumeroQuestao = int(st.slider("Digite uma questão:"   , min_value=1,    max_value=180))  
    
    Dominio = "https://api.enem.dev"
    Questao = RequestTextoQuestao(AnoQuestao, NumeroQuestao)
    ImprimirQuestao(Questao, QuebraComponentesQuestao(Questao, Questao["context"], 0), Dominio)


main()
