# Front-end do Alerta Golpe
# Rodar (dentro da pasta frontend): streamlit run app.py
import streamlit as st

from features import dicas, historico, verificar
from providers import api_cliente
from state import sessao

st.set_page_config(page_title="Alerta Golpe", page_icon="🛡️", layout="wide")
sessao.iniciar()

st.title("🛡️ Alerta Golpe")

aba_verificar, aba_historico, aba_dicas = st.tabs(["🔍 Verificar mensagem", "📊 Meu histórico", "💡 Como se proteger"])
with aba_verificar:
    verificar.mostrar()
with aba_historico:
    historico.mostrar()
with aba_dicas:
    dicas.mostrar()

# a barra lateral vem por último pra já enxergar o histórico atualizado nesta execução
with st.sidebar:
    st.header("🛡️ Alerta Golpe")
    st.write("Veja se uma mensagem tem cara de golpe antes de clicar ou pagar.")

    if api_cliente.api_online():
        st.success("🟢 Serviço funcionando")
    else:
        st.error("🔴 Serviço fora do ar agora. Tente mais tarde.")

    st.markdown("**Como funciona**")
    st.markdown("1. Você cola a mensagem\n2. A IA analisa\n3. Você vê o risco e o que fazer\n4. Você diz se a análise ajudou")

    st.markdown("**Sua privacidade**")
    st.caption("Não cole senhas. CPF, telefone, e-mail e número de cartão são escondidos antes de ir para a IA. "
               "O texto da mensagem não é gravado em arquivo nem em banco de dados.")

    if st.button("🗑️ Apagar meu histórico", disabled=not st.session_state.historico):
        sessao.limpar()
        st.rerun()
