# Componentes visuais reutilizáveis
import html

import streamlit as st

# cores com contraste alto (texto escuro em fundo claro) e sempre com ícone + texto junto
NIVEIS = {
    "alto": {"rotulo": "Risco alto", "icone": "🚨", "cor": "#B71C1C", "fundo": "#FDECEA",
             "frase": "Tem muita cara de golpe. Não clique em links e não mande dinheiro."},
    "medio": {"rotulo": "Risco médio", "icone": "⚠️", "cor": "#8A4B00", "fundo": "#FFF4E5",
              "frase": "Tem sinais suspeitos. Confirme por outro meio antes de fazer qualquer coisa."},
    "baixo": {"rotulo": "Risco baixo", "icone": "✅", "cor": "#1B5E20", "fundo": "#EDF7ED",
              "frase": "Não encontramos sinais fortes de golpe, mas fique atento."},
}

# mesmas cores usadas nos gráficos
CORES_GRAFICO = {NIVEIS[n]["rotulo"]: NIVEIS[n]["cor"] for n in NIVEIS}


def rotulo_nivel(nivel):
    return f"{NIVEIS[nivel]['icone']} {NIVEIS[nivel]['rotulo']}"


def cartao_risco(nivel, titulo, detalhe="", compacto=False):
    # compacto=True é a versão menor usada no histórico
    n = NIVEIS[nivel]
    tamanho = "1.1rem" if compacto else "1.7rem"
    frase = "" if compacto else f"<div>{n['frase']}</div>"
    # html.escape porque o título vem da IA
    st.markdown(
        f"<div role='status' style='border-left:8px solid {n['cor']}; background:{n['fundo']}; color:#1A1A1A; "
        f"padding:12px 16px; border-radius:8px; margin-bottom:10px'>"
        f"<div style='font-size:{tamanho}; font-weight:700; color:{n['cor']}'>{n['icone']} {n['rotulo']}</div>"
        f"{frase}<b>{html.escape(titulo)}</b><br><small>{html.escape(detalhe)}</small></div>",
        unsafe_allow_html=True,
    )


def lista_com_icone(titulo, itens, icone, texto_vazio="Nada para mostrar aqui."):
    st.markdown(f"**{titulo}**")
    if not itens:
        st.caption(texto_vazio)
        return
    for item in itens:
        st.markdown(f"{icone} {item}")


def estado_vazio(texto, icone="📭"):
    st.info(f"{icone} {texto}")


def caixa_erro(texto):
    st.error(f"😕 {texto}")
    st.caption("Enquanto isso: na dúvida, não clique em links e não faça Pix. Ligue para a pessoa ou para o banco pelo número oficial.")
