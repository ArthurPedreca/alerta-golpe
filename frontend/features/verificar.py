# Tela "Verificar mensagem": entrada do cidadão, resultado da IA e avaliação (human-in-the-loop)
from datetime import datetime

import streamlit as st

from providers import api_cliente
from providers.api_cliente import ErroAPI
from state import sessao
from ui import componentes

CANAIS = ["WhatsApp", "SMS", "E-mail", "Ligação", "Rede social", "Outro"]
PEDE_DINHEIRO = {"Sim": "sim", "Não": "nao", "Não sei": "nao_sei"}


def validar(mensagem, canal):
    erros = []
    texto = (mensagem or "").strip()
    if not texto:
        erros.append("Cole a mensagem que você recebeu.")
    elif len(texto) < 10:
        erros.append("A mensagem está muito curta. Cole o texto completo (pelo menos 10 letras).")
    elif len(texto) > 2000:
        erros.append("A mensagem é muito grande. Cole só a parte principal (até 2000 letras).")
    if canal is None:
        erros.append("Escolha por onde a mensagem chegou.")
    return erros


def mostrar():
    st.subheader("Recebeu uma mensagem estranha?")
    st.write("Cole aqui antes de clicar em qualquer link ou fazer um Pix. A gente te ajuda a ver se tem cara de golpe.")

    # form: o Streamlit só roda de novo quando clicar no botão, e não a cada letra digitada
    with st.form("form_verificar"):
        mensagem = st.text_area(
            "Mensagem recebida",
            placeholder="Exemplo: Oi, troquei de número. Salva esse aqui. Pode me fazer um Pix hoje?",
            height=170,
            max_chars=2000,
            help="Copie e cole o texto da mensagem. Se quiser, apague seu nome antes.",
        )
        col1, col2 = st.columns(2)
        canal = col1.selectbox("Por onde a mensagem chegou?", CANAIS, index=None, placeholder="Escolha uma opção")
        pede = col2.radio("Ela pede dinheiro, Pix, senha ou código?", list(PEDE_DINHEIRO), index=2, horizontal=True)
        enviar = st.form_submit_button("🔍 Verificar mensagem", type="primary")

    if enviar:
        erros = validar(mensagem, canal)
        if erros:
            for erro in erros:
                st.warning(f"✏️ {erro}")
            return
        with st.spinner("Analisando a mensagem com inteligência artificial... isso leva alguns segundos."):
            try:
                resultado = api_cliente.analisar_mensagem(mensagem.strip(), canal, PEDE_DINHEIRO[pede])
            except ErroAPI as erro:
                componentes.caixa_erro(str(erro))
                return
        if not sessao.adicionar(resultado):
            st.info("ℹ️ Você já tinha verificado essa mensagem. Mostrando o mesmo resultado, sem chamar a IA de novo.")

    item = sessao.ultima_analise()
    if item is None:
        componentes.estado_vazio("Nenhuma mensagem verificada ainda. O resultado vai aparecer aqui.")
        return
    mostrar_resultado(item)


def mostrar_resultado(item):
    analise = item["analise"]
    hora = datetime.fromisoformat(item["criado_em"]).strftime("%d/%m %H:%M")

    st.subheader("Resultado")
    componentes.cartao_risco(analise["nivel_risco"], analise["tipo_golpe"], f"Protocolo {item['protocolo']} • {item['canal']} • {hora}")
    st.write(analise["resumo"])
    if item["ajustado_pela_regra"]:
        st.caption("ℹ️ Subimos o nível para médio porque você disse que a mensagem pede dinheiro, Pix, senha ou código.")

    col1, col2 = st.columns(2)
    with col1:
        componentes.lista_com_icone("Sinais de alerta", analise["sinais_alerta"], "⚠️", "A IA não encontrou sinais de alerta.")
    with col2:
        componentes.lista_com_icone("O que fazer agora", analise["o_que_fazer"], "👉")
    componentes.lista_com_icone("Onde pedir ajuda", item["onde_pedir_ajuda"], "📞", "Nenhuma ação extra necessária.")

    st.caption("Esta análise foi feita por inteligência artificial e pode errar. Na dúvida, desconfie e confirme por outro meio.")
    avaliacao(item)


def avaliacao(item):
    """Human-in-the-loop: o cidadão confirma ou corrige o resultado da IA"""
    st.divider()
    st.subheader("Essa análise está certa?")
    protocolo = item["protocolo"]

    aviso = st.session_state.pop("aviso_feedback", None)
    if aviso:
        st.warning(aviso)

    if item["avaliacao"]:
        texto = f"Obrigado! Você marcou esta análise como **{item['avaliacao']}**."
        if item["nivel_final"] != item["analise"]["nivel_risco"]:
            texto += f" No seu histórico ela aparece como {componentes.rotulo_nivel(item['nivel_final'])}."
        st.success(texto)
        return

    resposta = st.radio("O que você achou do resultado?", ["Está certa", "Está errada"], index=None,
                        horizontal=True, key=f"aval_{protocolo}")
    nivel_correto = None
    if resposta == "Está errada":
        nivel_correto = st.selectbox("Na sua opinião, qual seria o nível certo?", ["alto", "medio", "baixo"],
                                     format_func=componentes.rotulo_nivel, index=None,
                                     placeholder="Escolha o nível", key=f"nivel_{protocolo}")
    comentario = st.text_input("Quer explicar? (opcional)", max_chars=300, key=f"coment_{protocolo}",
                               help="Não escreva dados pessoais aqui.")

    if st.button("Enviar avaliação", key=f"btn_{protocolo}", disabled=resposta is None):
        if resposta == "Está errada" and nivel_correto is None:
            st.warning("✏️ Escolha qual seria o nível certo.")
            return
        util = resposta == "Está certa"
        try:
            api_cliente.enviar_feedback(protocolo, item["analise"]["nivel_risco"], util, nivel_correto, comentario)
        except ErroAPI:
            st.session_state.aviso_feedback = "Não conseguimos enviar sua avaliação agora, mas ela ficou guardada no seu histórico."
        sessao.registrar_avaliacao(protocolo, util, nivel_correto)
        st.rerun()
