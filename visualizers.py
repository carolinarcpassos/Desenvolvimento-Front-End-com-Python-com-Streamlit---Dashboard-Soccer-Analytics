"""
==============================================================================
ARQUIVO: visualizers.py
OBJETIVO: Módulo de Geração de Visualizações de Dados e Gráficos Táticos
==============================================================================
"""

import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch, PyPizza
import seaborn as sns
import pandas as pd


# ==============================================================================
# Tarefa: Criar visualizações de dados - Utilizar mplsoccer (Mapa de Chutes)
# Utiliza a biblioteca mplsoccer para gerar um mapa de chutes interativo sobre o campo,
# com legendas e destaques visuais para finalizações convertidas em gols.
# ==============================================================================
def gerar_mapa_chutes(events_df, time_nome=None):
    """
    Gera um mapa de chutes utilizando Pitch da mplsoccer.

    Args:
        events_df (pd.DataFrame): DataFrame de eventos da partida.
        time_nome (str, optional): Nome do time selecionado para filtro.

    Returns:
        plt.Figure: Objeto contendo o gráfico de chutes plotado sobre o campo.
    """
    chutes = events_df[events_df['type'] == 'Shot'].copy()
    if time_nome:
        chutes = chutes[chutes['team'] == time_nome]

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1d24', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(8, 6))

    gols = chutes[chutes['shot_outcome'] == 'Goal']
    nao_gols = chutes[chutes['shot_outcome'] != 'Goal']

    pitch.scatter(nao_gols['x'], nao_gols['y'], alpha=0.6, s=100, color='red', label='Chute sem gol', ax=ax)
    pitch.scatter(gols['x'], gols['y'], alpha=0.9, s=200, color='gold', marker='*', label='Gol', ax=ax)

    ax.set_title(f"Mapa de Chutes - {time_nome if time_nome else 'Geral'}", fontsize=12, color='white')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)
    return fig


# ==============================================================================
# Tarefa: Criar visualizações de dados - Utilizar mplsoccer (Mapa de Passes)
# Gera um mapa espacial de passes utilizando vetores/setas direcionais para indicar
# a trajetória e distribuição dos passes efetuados por uma equipe ou jogador.
# ==============================================================================
def gerar_mapa_passes(events_df, jogador_nome=None):
    """
    Gera mapa de passes com setas direcionais.

    Args:
        events_df (pd.DataFrame): DataFrame de eventos.
        jogador_nome (str, optional): Nome do jogador selecionado.

    Returns:
        plt.Figure: Objeto contendo o mapa de passes direcionais.
    """
    passes = events_df[events_df['type'] == 'Pass'].copy()
    if jogador_nome:
        passes = passes[passes['player'] == jogador_nome]

    passes[['end_x', 'end_y']] = pd.DataFrame(passes['pass_end_location'].tolist(), index=passes.index)

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1d24', line_color='#e1e8e3')
    fig, ax = pitch.draw(figsize=(6, 6))
    pitch.arrows(passes['x'], passes['y'], passes['end_x'], passes['end_y'], color='#2bb673', ax=ax, width=2)
    ax.set_title(f"Mapa de Passes: {jogador_nome if jogador_nome else 'Todos'}", fontsize=12, color='white')
    return fig


# ==============================================================================
# Tarefa: Novas visualizações de acordo com a galeria da mplsoccer (PyPizza)
# Utiliza a classe PyPizza da galeria oficial do mplsoccer para construir gráficos 
# de pizza/radar detalhando o perfil de ações do atleta selecionado.
# ==============================================================================
def gerar_pizza_chart_mplsoccer(events_df, jogador_nome):
    """
    Gera gráfico da Galeria do mplsoccer: PyPizza de Ações do Jogador.

    Args:
        events_df (pd.DataFrame): DataFrame de eventos da partida.
        jogador_nome (str): Nome do atleta analisado.

    Returns:
        plt.Figure: Gráfico estilo PyPizza com a distribuição das ações táticas.
    """
    df_jog = events_df[events_df['player'] == jogador_nome]
    
    passes = len(df_jog[df_jog['type'] == 'Pass'])
    chutes = len(df_jog[df_jog['type'] == 'Shot'])
    desarmes = len(df_jog[df_jog['type'].isin(['Duel', 'Interception'])])
    
    params = ["Passes", "Chutes", "Desarmes/Interceptações"]
    values = [passes, chutes, desarmes]
    
    baker = PyPizza(params=params, straight_line_color="#000000", last_circle_lw=1)
    fig, ax = baker.make_pizza(values, figsize=(4.5, 4.5), param_location=110)
    fig.suptitle(f"Perfil de Ações: {jogador_nome}", fontsize=14)
    return fig


# ==============================================================================
# Tarefa: Criar visualizações adicionais com Matplotlib e Seaborn
# Gera um gráfico de dispersão temporal utilizando Seaborn para analisar a relação
# e volume de ocorrências (passes, chutes, faltas) ao longo do tempo de jogo.
# ==============================================================================
def gerar_relacao_seaborn(events_df):
    """
    Visualização Seaborn: Relação entre Tipo de Evento e Distribuição Temporal por Minuto.

    Args:
        events_df (pd.DataFrame): DataFrame de eventos do confronto.

    Returns:
        plt.Figure: Gráfico de dispersão com Seaborn.
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    sub_df = events_df[events_df['type'].isin(['Pass', 'Shot', 'Foul Committed', 'Duel'])]
    
    sns.scatterplot(data=sub_df, x='minute', y='type', hue='team', alpha=0.7, ax=ax)
    ax.set_title("Seaborn: Distribuição Temporal de Eventos por Time")
    ax.set_xlabel("Minuto do Jogo")
    ax.set_ylabel("Tipo de Evento")
    plt.tight_layout()
    return fig