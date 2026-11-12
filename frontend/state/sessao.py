# Estado centralizado da sessão do cidadão (histórico e última análise)
import pandas as pd
import streamlit as st


def iniciar():
    st.session_state.setdefault("historico", [])  # lista de análises feitas nesta sessão
    st.session_state.setdefault("ultima", None)  # protocolo da última análise mostrada


def adicionar(resultado):
    """Coloca a análise no histórico. Retorna False se ela já estava lá (veio do cache)"""
    st.session_state.ultima = resultado["protocolo"]
    for item in st.session_state.historico:
        if item["protocolo"] == resultado["protocolo"]:
            return False
    item = dict(resultado)
    item["avaliacao"] = None  # "útil" ou "incorreta", preenchido pelo cidadão
    item["nivel_final"] = resultado["analise"]["nivel_risco"]
    st.session_state.historico.append(item)
    return True


def pegar(protocolo):
    for item in st.session_state.historico:
        if item["protocolo"] == protocolo:
            return item
    return None


def ultima_analise():
    if st.session_state.ultima:
        return pegar(st.session_state.ultima)
    return None


def registrar_avaliacao(protocolo, util, nivel_correto):
    item = pegar(protocolo)
    if item is None:
        return
    item["avaliacao"] = "útil" if util else "incorreta"
    if not util and nivel_correto:
        item["nivel_final"] = nivel_correto  # vale o que o cidadão corrigiu


def limpar():
    st.session_state.historico = []
    st.session_state.ultima = None


def historico_df():
    linhas = []
    for item in st.session_state.historico:
        linhas.append({
            "protocolo": item["protocolo"],
            "data": pd.to_datetime(item["criado_em"]),
            "canal": item["canal"],
            "tipo_golpe": item["analise"]["tipo_golpe"],
            "nivel_ia": item["analise"]["nivel_risco"],
            "nivel_final": item["nivel_final"],
            "avaliacao": item["avaliacao"] or "sem avaliação",
        })
    return pd.DataFrame(linhas)
