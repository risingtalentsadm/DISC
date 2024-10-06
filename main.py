import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Ler os dados da planilha
url = "https://docs.google.com/spreadsheets/d/1ibFCdRfpYA5SapBJ6kc9tG44_SXGfYoyKC5_xGDMZs8/gviz/tq?tqx=out:csv&gid=1991638792"
df = pd.read_csv(url)

# Função para plotar o gráfico de um participante selecionado
def plotar_grafico(nome_pessoa):
    # Encontrar o índice do participante
    index = df[df.iloc[:, 1] == nome_pessoa].index[0]  # Segunda coluna com os nomes

    # Inicializar variáveis para cada perfil
    total_D, total_I, total_S, total_C = 0, 0, 0, 0
    total_respostas = 0  # Para calcular a porcentagem

    # Iterar sobre as colunas a partir da 5ª coluna (questões)
    for j in range(4, df.shape[1]):
        response = df.iat[index, j]
        if pd.notna(response):  # Verificar se a resposta não é NaN
            total_respostas += float(response)
            if (j - 4) % 4 == 0:  # D
                total_D += float(response)
            elif (j - 4) % 4 == 1:  # I
                total_I += float(response)
            elif (j - 4) % 4 == 2:  # S
                total_S += float(response)
            elif (j - 4) % 4 == 3:  # C
                total_C += float(response)

    # Calcular porcentagens
    if total_respostas > 0:
        porcentagens = [
            (total_D / 100) * 100,
            (total_I / 100) * 100,
            (total_S / 100) * 100,
            (total_C / 100) * 100
        ]
    else:
        porcentagens = [0, 0, 0, 0]  # Evitar divisão por zero

    # Criar uma lista com os totais de cada perfil
    labels = ['D (Dominância)', 'I (Influência)', 'S (Estabilidade)', 'C (Conformidade)']

    # Plotar o gráfico de barras para o participante selecionado
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, porcentagens, color=['purple', 'blue', 'green', 'orange'])
    ax.set_title(f'Porcentagem dos Perfis DISC - {nome_pessoa}')
    ax.set_xlabel('Perfis DISC')
    ax.set_ylabel('Porcentagem (%)')
    ax.set_ylim(0, 100)  # Definir o limite do eixo Y
    ax.grid(True, axis='y')

    # Mostrar o gráfico para o participante selecionado
    st.pyplot(fig)

    # Criar uma tabela com as porcentagens
    tabela_dados = pd.DataFrame({
        'Perfil': labels,
        'Porcentagem': porcentagens
    })
    st.write("### Tabela de Porcentagens")
    st.table(tabela_dados)

# Configuração da interface Streamlit
st.title("Análise de Perfis DISC")
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha a Página", ["Bem-vindo", "Gráficos Individuais"])

if page == "Bem-vindo":
    st.header("Bem-vindo ao Analisador de Perfis DISC!")
    st.write("Esta aplicação permite visualizar os perfis DISC dos participantes do questionário.")
    st.write("Use o menu lateral para navegar entre as páginas.")

elif page == "Gráficos Individuais":
    st.header("Gráficos dos Participantes")

    # Criar um selectbox para escolher o participante
    nomes = df.iloc[:, 1].unique()  # Obter os nomes únicos da segunda coluna
    nome_selecionado = st.selectbox("Selecione um participante:", nomes)

    # Botão para gerar o gráfico
    if st.button("Gerar Gráfico"):
        plotar_grafico(nome_selecionado)

