"""
==============================================================================
ARQUIVO: data_loader.py
OBJETIVO: Carregamento de Dados da StatsBomb e Pré-processamento
==============================================================================
"""

import streamlit as st
import pandas as pd
from statsbombpy import sb


# ==============================================================================
# Tarefa: Implementar funcionalidades avançadas - Utilizar o Cache do Streamlit
# Utiliza @st.cache_data para otimizar o carregamento de dados da API da StatsBomb,
# evitando requisições repetidas a cada interação do usuário no dashboard.
# ==============================================================================

@st.cache_data(ttl=600, show_spinner=False)
def carregar_competicoes():
    """
    Carrega as competições disponíveis na base de dados aberta da StatsBomb.

    Returns:
        pd.DataFrame: Lista de campeonatos e competições ativas.
    """
    return sb.competitions()


@st.cache_data(ttl=600, show_spinner=False)
def carregar_partidas(competition_id, season_id):
    """
    Carrega as partidas de uma competição e temporada específicas.

    Args:
        competition_id (int): ID da competição.
        season_id (int): ID da temporada.

    Returns:
        pd.DataFrame: Lista de partidas com dados de equipes e resultados.
    """
    return sb.matches(competition_id=competition_id, season_id=season_id)


@st.cache_data(ttl=600, show_spinner=False)
def carregar_eventos_partida(match_id):
    """
    Carrega e trata os eventos de uma partida específica.

    Tratamento e Sanitização de Dados:
    - Trata valores ausentes ou não-lista na coluna 'location' para evitar falhas de
      atribuição de dimensão (ValueError) em eventos sem coordenadas (ex: substituições).
    - Extrai as coordenadas X e Y em colunas separadas para plotagens geográficas.

    Args:
        match_id (int): ID da partida.

    Returns:
        pd.DataFrame: DataFrame contendo eventos detalhados e coordenadas X, Y.
    """
    events = sb.events(match_id=match_id)
    
    # Preenche valores ausentes ou não-lista na coluna 'location'
    events['location'] = events['location'].apply(
        lambda x: x if isinstance(x, list) and len(x) == 2 else [None, None]
    )
    
    # Extrai as coordenadas X e Y
    events[['x', 'y']] = pd.DataFrame(events['location'].tolist(), index=events.index)
    
    return events