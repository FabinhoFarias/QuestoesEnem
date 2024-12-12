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
        if st.button(f"Alternativa {Alternativa['letter']}"):
            if Alternativa["isCorrect"]:
                st.write(f"Alternativa CORRETA :)")
            else:
                st.write(f"Alternativa ERRADA :(")
        if Alternativa["text"]: #Se houver texto
            st.write(f"{Alternativa["text"]}")
        else: # há imagem
            st.image(Alternativa["file"], caption="Alternativa")

    # Exemplo de dados de uma questão
    QUESTAO = {
        "alternatives": [
            {"letter": "A", "text": "50 minutos.", "file": None, "isCorrect": False},
            {"letter": "B", "text": None, "file": "https://via.placeholder.com/150", "isCorrect": True},
            {"letter": "C", "text": "80 minutos.", "file": None, "isCorrect": False},
            {"letter": "D", "text": None, "file": "https://via.placeholder.com/200", "isCorrect": False},
        ]
    }

    # Laço para renderizar as alternativas
    for Alternativa in QUESTAO["alternatives"]:
        st.markdown("---")  # Divisor entre alternativas
        
        if Alternativa["file"]:  # Caso tenha imagem
            # Botão com imagem usando HTML
            st.markdown(
                f"""
                <a href="#" onclick="window.location.reload()" class="button">
                    <img src="{Alternativa['file']}" alt="Alternativa {Alternativa['letter']}" style="width:150px; height:auto; border-radius:10px;"/>
                </a>
                """,
                unsafe_allow_html=True,
            )
            st.write(f"Alternativa {Alternativa['letter']}")
        else:  # Caso tenha texto
            if st.button(f"Alternativa {Alternativa['letter']} - {Alternativa['text']}"):
                if Alternativa["isCorrect"]:
                    st.write(f"Alternativa CORRETA :)")
                else:
                    st.write(f"Alternativa ERRADA :(")

    st.markdown("---")  # Divisor final



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
