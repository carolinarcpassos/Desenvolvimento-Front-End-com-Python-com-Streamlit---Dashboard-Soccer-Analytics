# 📊 Dashboard Analítico de Soccer Analytics (StatsBomb & Streamlit)

Este repositório contém o desenvolvimento de uma aplicação web interativa em **Streamlit** focada na análise exploratória de dados de futebol da plataforma **StatsBomb**. O projeto foi construído de forma incremental e modular, aplicando diversas bibliotecas do ecossistema de Ciência de Dados em Python para responder a perguntas táticas e performáticas de partidas e jogadores.


📂 Estrutura do Projeto
├── app.py                  # Código-fonte principal com a interface e layout do dashboard
├── data_loader.py          # Funções de carregamento de dados (StatsBombPy com Cache)
├── visualizers.py          # Módulo para criação dos mapas e gráficos (mplsoccer, seaborn e matplotlib)
├── .gitignore              # Configuração para ignorar arquivos de sistema e ambientes virtuais (venv/)
├── requirements.txt        # Bibliotecas e dependências do projeto para replicação do ambiente
└── README.md               # Documentação do projeto (este arquivo)


📥 Fonte dos Dados (StatsBomb)
Os dados utilizados na aplicação foram obtidos diretamente da API pública da StatsBomb via biblioteca statsbombpy:   - Tabela Utilizada: Dados abertos de competições, temporadas, partidas e eventos detalhados.   
- Formato do Arquivo: Requisições de API convertidas dinamicamente em DataFrames do Pandas.   
- Conteúdo: Eventos minuto a minuto de partidas (passes, finalizações, desarmes, coordenadas X/Y de localização e desfechos de jogadas).   
- Link de acesso: https://github.com/statsbomb/statsbombpy


🚀 Como Executar o Projeto Localmente (Linux / Windows)
Siga os passos abaixo no terminal do seu sistema para configurar o ambiente e rodar o aplicativo:   
- Clonar o Repositório
    git clone https://github.com/carolinarcpassos/Desenvolvimento-Front-End-com-Python-com-Streamlit---Dashboard-Soccer-Analytics.git
    cd Desenvolvimento-Front-End-com-Python-com-Streamlit---Dashboard-Soccer-Analytics

- Criar e Ativar o Ambiente Virtual
    - Linux / Mac:
        python3 -m venv .venv
        source .venv/bin/activate
    - Windows:
        python -m venv .venv
        .venv\Scripts\activate

- Instalar as Dependências
    pip install --upgrade pip
    pip install -r requirements.txt

- Executar o Dashboard
    streamlit run app.py

A aplicação abrirá automaticamente no seu navegador padrão em http://localhost:8501.  


🎯 Exercícios Implementados no Dashboard

Pergunta Central do Dashboard:
"Qual é o perfil de construção tática da equipe vitoriosa e como a eficiência dos chutes se relaciona com a distribuição espacial dos passes ao longo dos 90 minutos?

Exercício 1: Preparar o Ambiente de Desenvolvimento
Prático:
Criação e ativação do ambiente virtual isolado (venv), instalação do conjunto de bibliotecas necessárias (streamlit, statsbombpy, mplsoccer, matplotlib, seaborn, pandas) e geração do arquivo de requisitos.   

Exercício 2: Estruturar o Projeto e Repositório GitHub
Prático:
Organização modular do código em arquivos separados (app.py, data_loader.py e visualizers.py), configuração do arquivo requirements.txt e versionamento inicial do repositório no GitHub.   

Exercício 3: Definir a Estrutura do Dashboard
Prático:
Construção da interface interativa no Streamlit utilizando st.sidebar com seletores encadeados em cascata para permitir ao usuário escolher uma competição, uma temporada e uma partida/jogador específicos, organizando o layout com st.columns, st.container e st.tabs.   

Exercício 4: Obter Dados e Exibir Informações Básicas
Prático:
Consumo dos dados abertos da StatsBomb via statsbombpy exibindo os metadados da partida selecionada, estatísticas básicas do jogo e uma tabela interativa (st.dataframe) com os eventos de passes, finalizações e desarmes.   

Exercício 5: Criar Visualizações de Dados (mplsoccer)
Prático:
Geração de mapas de passes (com trajetórias e setas) e mapas de chutes (com marcações destacando os gols) utilizando a biblioteca mplsoccer em campos do tipo Pitch.   

Exercício 6: Visualizações Avançadas e Galeria
Prático:
Desenvolvimento de gráficos adicionais com Seaborn para correlacionar o volume de eventos ao longo do tempo e implementação de gráfico de pizza/radar (PyPizzas) inspirado na galeria oficial do mplsoccer.   

Exercício 7: Adicionar Interatividade e Seletores de Jogador
Prático:
Inclusão de seletores individuais por jogador na interface, ajustando os gráficos do campo dinamicamente conforme a seleção do usuário.   

Exercício 8: Desenvolver Serviço de Download de Arquivos
Prático:
Implementação do botão de exportação st.download_button permitindo ao usuário baixar a tabela de eventos filtrados diretamente em formato CSV.   

Exercício 9: Utilizar Barra de Progresso e Spinners
Prático:
Adição de barra de progresso (st.progress) e spinners de carregamento (st.spinner) para fornecer feedback visual durante o consumo e o processamento dos dados da API.   

Exercício 10: Exibir Métricas e Indicadores
Prático:
Construção de cartões de métricas (st.metric) com variações coloridas (delta) exibindo dados consolidados como total de gols, total de chutes e taxa de conversão.   

Exercício 11: Criar Formulários Interativos
Prático:
Desenvolvimento de formulários agrupados (st.form) utilizando st.text_input, st.radio, st.slider e st.checkbox para filtrar os eventos por intervalo de tempo e atletas.   

Exercício 12: Implementar Cache e Session State
Prático:
Aplicação do decorador @st.cache_data para otimizar as chamadas da API da StatsBomb e utilização de st.session_state para manter os dados da partida salvos durante a navegação.   


👤 Carolina Passos - Git: carolinarcpassos/Desenvolvimento-Front-End-com-Python-com-Streamlit---Dashboard-Soccer-Analytics.git