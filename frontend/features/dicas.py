# Tela "Como se proteger": tipos de golpe (vem da API, com cache) e dicas fixas
import streamlit as st

from providers import api_cliente
from providers.api_cliente import ErroAPI
from ui import componentes

REGRAS = [
    "Desconfie de pressa, ameaça ou de oferta boa demais.",
    "Banco não liga pedindo senha, código do SMS ou Pix de teste.",
    "Pedido de dinheiro de parente ou amigo? Ligue para a pessoa no número que você já tinha.",
    "Não clique em links de mensagens que você não esperava. Digite o endereço do site você mesmo.",
    "Ative a confirmação em duas etapas no WhatsApp.",
]


def mostrar():
    st.subheader("Golpes mais comuns")
    st.caption("Em 2025 o Brasil registrou mais de 2,2 milhões de estelionatos, uma média de 258 por hora (20º Anuário Brasileiro de Segurança Pública).")
    try:
        tipos = api_cliente.listar_tipos_golpe()
    except ErroAPI as erro:
        componentes.caixa_erro(str(erro))
        tipos = []
    for tipo in tipos:
        with st.expander(tipo["tipo"]):
            st.write(tipo["descricao"])

    st.subheader("Regras de ouro")
    componentes.lista_com_icone("Para não cair em golpe:", REGRAS, "✔️")
