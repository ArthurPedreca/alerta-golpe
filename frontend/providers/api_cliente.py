# Cliente HTTP da nossa API. O front nunca fala com a OpenAI, só com o back-end
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
TIMEOUT = 40  # segundos (a IA pode levar uns 10 s)

NIVEIS_VALIDOS = {"baixo", "medio", "alto"}


class ErroAPI(Exception):
    # o texto do erro já é a mensagem que aparece pro cidadão
    pass


@st.cache_resource
def _sessao_http():
    # uma sessão só pra reaproveitar a conexão entre os reruns
    return requests.Session()


def _chamar(metodo, caminho, dados=None, timeout=TIMEOUT):
    try:
        resposta = _sessao_http().request(metodo, API_URL + caminho, json=dados, timeout=timeout)
    except requests.exceptions.Timeout:
        raise ErroAPI("A análise demorou mais que o normal. Espere um pouco e tente de novo.")
    except requests.exceptions.ConnectionError:
        api_online.clear()  # limpa o cache do status pra barra lateral já mostrar "fora do ar"
        raise ErroAPI("Não conseguimos falar com o serviço agora. Ele pode estar fora do ar. Tente de novo em alguns minutos.")

    if resposta.status_code == 422:
        raise ErroAPI("Não deu para entender o que foi enviado. Confira o texto da mensagem e tente de novo.")
    if resposta.status_code == 504:
        raise ErroAPI("A inteligência artificial demorou demais para responder. Tente de novo.")
    if resposta.status_code in (502, 503):
        raise ErroAPI("A inteligência artificial está com problema agora. Tente de novo daqui a pouco.")
    if resposta.status_code >= 400:
        raise ErroAPI("Algo deu errado do nosso lado. Tente de novo mais tarde.")

    try:
        return resposta.json()
    except ValueError:
        raise ErroAPI("Recebemos uma resposta estranha do serviço. Tente de novo.")


@st.cache_data(ttl=1800, max_entries=100, show_spinner=False)
def analisar_mensagem(mensagem, canal, pede_dinheiro):
    # cache: se a mesma mensagem for enviada de novo, não chama a IA outra vez (fica 30 min só na memória)
    dados = _chamar("POST", "/v1/analises", {"mensagem": mensagem, "canal": canal, "pede_dinheiro": pede_dinheiro})

    # confere se veio no formato esperado antes de mostrar
    if "protocolo" not in dados or dados.get("analise", {}).get("nivel_risco") not in NIVEIS_VALIDOS:
        raise ErroAPI("Recebemos uma resposta incompleta do serviço. Tente de novo.")
    return dados


def enviar_feedback(protocolo, nivel_ia, util, nivel_correto, comentario):
    _chamar("POST", "/v1/feedback", {
        "protocolo": protocolo,
        "nivel_ia": nivel_ia,
        "util": util,
        "nivel_correto": nivel_correto,
        "comentario": comentario or None,
    }, timeout=10)


@st.cache_data(ttl=3600, show_spinner=False)
def listar_tipos_golpe():
    return _chamar("GET", "/v1/tipos-golpe", timeout=10)


@st.cache_data(ttl=10, show_spinner=False)
def api_online():
    try:
        _chamar("GET", "/health", timeout=3)
        return True
    except ErroAPI:
        return False
