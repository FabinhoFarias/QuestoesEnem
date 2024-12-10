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
        ListaPivo = TextoQuestao.split(f"![]({QuestaoJson['files'][contador]})")
        ListaComponentesQuestao.append(ListaPivo[0])
        ListaComponentesQuestao.append(QuestaoJson["files"][contador])
        contador += 1
        if ListaPivo[-1]:
            return QuebraComponentesQuestao(QuestaoJson, ListaPivo[-1], contador)

def ImprimirQuestao(ListaComponentesQuestao, DOMINIO):
    for Componente in ListaComponentesQuestao:
        if DOMINIO in Componente:
            print("\n")
            st.image(Componente, caption="Imagem da Questão")
            print("\n")
        else:
            st.write(Componente)
            print("\n")
        #Implementar o LaTeX depois


    # st.html(f"{Questao["context"]}")
    # if len(Questao["files"]) >= 1:
    #     for Arquivo in Questao["files"]:
    #         st.image(f"{Arquivo}")        
    # st.html(f"<p>{Questao["alternativesIntroduction"]}</p>")



def main():
    if "page" not in st.session_state:
        st.session_state.page = "PaginaInicial"

    def NavegarEntrePaginas(pagina):
        st.session_state.page = pagina

    if st.session_state.page == "PaginaInicial":
        st.title("Sistema de Navegação no Streamlit")
        st.header("Selecione uma opção:")
        st.button("Ir para Página de Conteúdos", use_container_width=True, on_click=NavegarEntrePaginas, args=("PaginaDeConteudos"))
        st.button("Ir para Página de Listas", use_container_width=True, on_click=NavegarEntrePaginas, args=("PaginaDeListas"))

    elif st.session_state.page == "PaginaDeListas":
        pooo()  # Função do arquivo 'PaginaDeListas'
    AnoQuestao    = int(st.slider("Digite o Ano da Prova:", min_value=2009, max_value=2023))    
    NumeroQuestao = int(st.slider("Digite uma questão:"   , min_value=1, max_value=180))  
    
    Dominio = "https://api.enem.dev"
    Questao = RequestTextoQuestao(AnoQuestao, NumeroQuestao)
    ImprimirQuestao(QuebraComponentesQuestao(Questao, Questao["context"], 0), Dominio)


main()