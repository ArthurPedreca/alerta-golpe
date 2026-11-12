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
    """Cartão colorido com o nível de risco. compacto=True é a versão menor usada no histórico"""
    n = NIVEIS[nivel]
    tamanho = "1.1rem" if compacto else "1.7rem"
    frase = "" if compacto else f"<div style='font-size:1.05rem;margin-top:4px'>{n['frase']}</div>"
    padding = "10px 14px" if compacto else "18px 20px"
    # html montado sem espaço no começo das linhas, senão o markdown acha que é bloco de código
    partes = [
        f"<div role='status' aria-live='polite' style='border-left:8px solid {n['cor']}; background:{n['fundo']}; "
        f"color:#1A1A1A; padding:{padding}; border-radius:8px; margin-bottom:10px'>",
        f"<div style='font-size:{tamanho}; font-weight:700; color:{n['cor']}'>{n['icone']} {n['rotulo']}</div>",
        frase,
        f"<div style='margin-top:6px; font-weight:600'>{html.escape(titulo)}</div>",
        f"<div style='font-size:0.9rem; color:#333333'>{html.escape(detalhe)}</div>",
        "</div>",
    ]
    st.markdown("".join(partes), unsafe_allow_html=True)


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
