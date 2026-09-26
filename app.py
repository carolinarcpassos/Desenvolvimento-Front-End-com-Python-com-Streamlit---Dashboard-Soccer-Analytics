"""
==============================================================================
ARQUIVO: app.py
OBJETIVO: Interface Principal do Dashboard Interativo em Streamlit
==============================================================================
"""

import streamlit as st
import pandas as pd
import time

from data_loader import carregar_competicoes, carregar_partidas, carregar_eventos_partida
from visualizers import (
    gerar_mapa_chutes, 
    gerar_mapa_passes, 
    gerar_pizza_chart_mplsoccer, 
    gerar_relacao_seaborn
)

# Configuração da página e layout da aplicação
st.set_page_config(page_title="Soccer Analytics Dashboard", page_icon="⚽", layout="wide")


# ==============================================================================
# Tarefa: Implementar funcionalidades avançadas - Armazenar o Estado da Sessão
# Utiliza Session State do Streamlit para persistir o identificador da partida 
# e manter as escolhas do usuário salvas ao navegar pela aplicação.
# ==============================================================================
if 'partida_id' not in st.session_state:
    st.session_state['partida_id'] = None


# Título e Pergunta da Análise
st.title("⚽ Painel de Análise Tática e Desempenho Futebolístico")

st.write("")

# ==============================================================================
# Tarefa: Definir a estrutura do dashboard - Uso de Containers
# Organiza a exibição da pergunta investigativa do dashboard dentro de um container.
# ==============================================================================
with st.container():
    st.info(
        "📌 **Pergunta Central da Análise:** Qual é o perfil de construção tática das equipes "
        "e como o volume de passes se relaciona com a eficácia dos chutes na partida?"
    )

st.write("") 
st.write("")

# ==============================================================================
# Tarefa: Definir a estrutura do dashboard - Uso de Sidebars e Seletores
# Configura menus retráteis na lateral permitindo selecionar campeonato, temporada e partida.
# ==============================================================================
st.sidebar.header("⚙️ Seleção de Parâmetros da Partida que será Analisada")

st.sidebar.write("")

df_comp = carregar_competicoes()

# Seleção de Campeonato
comp_sel = st.sidebar.selectbox("Competição:", df_comp['competition_name'].unique())
df_comp_filtered = df_comp[df_comp['competition_name'] == comp_sel]

# Seleção de Temporada
temp_sel = st.sidebar.selectbox("Temporada:", df_comp_filtered['season_name'].unique())
row_sel = df_comp_filtered[df_comp_filtered['season_name'] == temp_sel].iloc[0]


# ==============================================================================
# Tarefa: Adicionar interatividade - Barras de Progresso e Spinners
# Exibe animação visual de progresso e indicativo de carregamento enquanto consome a API.
# ==============================================================================
progress_bar = st.sidebar.progress(0)
for percent in range(100):
    time.sleep(0.003)
    progress_bar.progress(percent + 1)

with st.spinner("Buscando partidas disponíveis..."):
    df_matches = carregar_partidas(int(row_sel['competition_id']), int(row_sel['season_id']))

# Seleção de Partida
df_matches['label'] = df_matches['home_team'] + " x " + df_matches['away_team'] + " (" + df_matches['match_date'] + ")"
match_label = st.sidebar.selectbox("Partida:", df_matches['label'])

match_row = df_matches[df_matches['label'] == match_label].iloc[0]
match_id = int(match_row['match_id'])
st.session_state['partida_id'] = match_id

# Carregamento de Eventos da Partida
df_events = carregar_eventos_partida(match_id)


# ==============================================================================
# Tarefa: Definir a estrutura do dashboard - Organização em Tabs (Abas)
# Organiza as seções analíticas do dashboard em diferentes abas.
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Resumo da Partida", 
    "🏟️ Chutes & Finalizações", 
    "📈 Passes & Estatísticas", 
    "⚔️ Comparativo de Jogadores"
])


# ==============================================================================
# Tarefa: Obter dados e exibir informações básicas / Incluir métricas e indicadores
# Apresenta nome das equipes, KPIs com a função metric() e DataFrame de eventos.
# ==============================================================================
with tab1:
    # Exibição dinâmica do título da partida com placar correto
    st.subheader(
        f"Resumo da Partida: {match_row['home_team']} {match_row['home_score']} "
        f"x {match_row['away_score']} {match_row['away_team']}"
    )
    
    total_chutes = len(df_events[df_events['type'] == 'Shot'])
    total_gols = int(match_row['home_score'] + match_row['away_score'])
    taxa_conv = (total_gols / total_chutes * 100) if total_chutes > 0 else 0

    # Estruturação em Colunas (columns)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de Gols", total_gols, delta=f"{total_gols} no jogo", delta_color="normal")
    c2.metric("Total de Chutes", total_chutes, delta="Ações de Ataque", delta_color="off")
    c3.metric("Taxa de Conversão", f"{taxa_conv:.1f}%", delta="Eficiência", delta_color="normal")
    c4.metric("Volume de Eventos", len(df_events))

    st.markdown("---")
    st.write("### 📋 Tabela de Eventos da Partida")
    
    # Exibição do DataFrame de eventos
    st.dataframe(
        df_events[['minute', 'team', 'player', 'type']], 
        use_container_width=True
)

# ABA 2: VISUALIZAÇÕES MPLSOCCER
with tab2:
    st.subheader("Mapa de Chutes por Equipe")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.pyplot(gerar_mapa_chutes(df_events, match_row['home_team']))
    with col_b:
        st.pyplot(gerar_mapa_chutes(df_events, match_row['away_team']))


# ==============================================================================
# Tarefa: Adicionar interatividade - Seletores de Jogadores
# Permite ao usuário selecionar um jogador para visualizar mapas de passes e estatísticas.
# ==============================================================================
with tab3:
    st.subheader("Linha do Tempo Tática: Mapeamento de Passes, Finalizações e Duelos")
    st.pyplot(gerar_relacao_seaborn(df_events))
    
    st.markdown("---")
    st.subheader("Análise Individual por Jogador")
    
    jogadores = df_events['player'].dropna().unique()
    jogador_sel = st.selectbox("Selecione um Jogador:", sorted(jogadores))
    
    if jogador_sel:
        col_pizza, col_pass = st.columns(2)
        
        with col_pizza:
            st.markdown("### Perfil de Ações Táticas")
            st.pyplot(gerar_pizza_chart_mplsoccer(df_events, jogador_sel), use_container_width=True)
            
        with col_pass:
            st.markdown("### Mapa Espacial de Passes")
            st.pyplot(gerar_mapa_passes(df_events, jogador_sel), use_container_width=True)


# ==============================================================================
# ABA 4: COMPARATIVO DE JOGADORES, FORMULÁRIO E DOWNLOAD
# Tarefa: Criar formulários interativos, comparativo e botões de download
# ==============================================================================
with tab4:
    st.subheader("⚔️ Análise Comparativa de Desempenho Individual")
    
    # Separação automática dos jogadores por equipe
    time_casa = match_row['home_team']
    time_fora = match_row['away_team']
    
    jogadores_casa = sorted(df_events[df_events['team'] == time_casa]['player'].dropna().unique())
    jogadores_fora = sorted(df_events[df_events['team'] == time_fora]['player'].dropna().unique())

    # Form para seleção e filtros temporais
    with st.form("form_comparativo"):
        c_jog1, c_jog2 = st.columns(2)
        
        with c_jog1:
            jog_casa_sel = st.selectbox(f"Selecione Jogador do {time_casa}:", jogadores_casa)
        with c_jog2:
            jog_fora_sel = st.selectbox(f"Selecione Jogador do {time_fora}:", jogadores_fora)
            
        st.markdown("---")
        tempo_jogo = st.radio("Período do Jogo:", ["Jogo Completo", "1º Tempo", "2º Tempo"], horizontal=True)
        minutos = st.slider("Intervalo de Minutos da Partida:", 0, 90, (0, 90))
        exibir_tabela = st.checkbox("Exibir Tabela de Eventos Filtrados", value=True)
        
        btn_sub = st.form_submit_button("🔍 Processar Comparativo e Filtros")
        
    if btn_sub:
        # Aplicação dos Filtros de Período e Minuto
        df_filtrado = df_events.copy()
        if tempo_jogo == "1º Tempo":
            df_filtrado = df_filtrado[df_filtrado['period'] == 1]
        elif tempo_jogo == "2º Tempo":
            df_filtrado = df_filtrado[df_filtrado['period'] == 2]
            
        df_filtrado = df_filtrado[(df_filtrado['minute'] >= minutos[0]) & (df_filtrado['minute'] <= minutos[1])]
        
        st.success(f"Filtro aplicado! Exibindo dados do intervalo de {minutos[0]}' a {minutos[1]}' min ({tempo_jogo}).")
        
        # Exibição do Gráfico Comparativo de Pizza lado a lado
        st.markdown("### 📊 Perfil Tático Comparativo")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown(f"**{jog_casa_sel}** ({time_casa})")
            st.pyplot(gerar_pizza_chart_mplsoccer(df_filtrado, jog_casa_sel))
            
        with col_p2:
            st.markdown(f"**{jog_fora_sel}** ({time_fora})")
            st.pyplot(gerar_pizza_chart_mplsoccer(df_filtrado, jog_fora_sel))
            
        # Tabela e Download dos dados dos dois jogadores selecionados
        df_duelo = df_filtrado[df_filtrado['player'].isin([jog_casa_sel, jog_fora_sel])]
        
        if exibir_tabela:
            st.markdown("---")
            st.markdown("### 📋 Tabela de Eventos dos Atletas Selecionados")
            st.dataframe(df_duelo[['minute', 'team', 'player', 'type']], use_container_width=True)
            
        # Botão de Download dos Dados em CSV
        csv = df_duelo.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados dos Jogadores Selecionados (CSV)", 
            data=csv, 
            file_name=f"comparativo_{jog_casa_sel}_vs_{jog_fora_sel}.csv", 
            mime="text/csv"
        )