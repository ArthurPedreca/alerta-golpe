# Tela "Meu histórico": gráfico Plotly e filtros com as mensagens verificadas na sessão
import plotly.express as px
import streamlit as st

from state import sessao
from ui import componentes
from ui.componentes import CORES_GRAFICO, NIVEIS


def mostrar():
    st.subheader("Mensagens que você já verificou")
    df = sessao.historico_df()
    if df.empty:
        componentes.estado_vazio("Seu histórico aparece aqui depois que você verificar a primeira mensagem.")
        return
    st.caption("O histórico fica só nesta sessão. Se fechar a página, ele é apagado. O nível mostrado já considera a sua avaliação.")

    col1, col2, col3 = st.columns(3)
    niveis = col1.multiselect("Filtrar por nível de risco", ["alto", "medio", "baixo"], default=["alto", "medio", "baixo"],
                              format_func=componentes.rotulo_nivel)
    canais_existentes = sorted(df["canal"].unique())
    canais = col2.multiselect("Filtrar por canal", canais_existentes, default=canais_existentes)
    agrupar = col3.radio("Ver o gráfico por", ["Tipo de golpe", "Canal"], horizontal=True)

    filtrado = df[df["nivel_final"].isin(niveis) & df["canal"].isin(canais)]
    if filtrado.empty:
        componentes.estado_vazio("Nenhuma mensagem com esses filtros. Tente marcar mais opções.", "🔎")
        return

    m1, m2, m3 = st.columns(3)
    m1.metric("Mensagens verificadas", len(filtrado))
    m2.metric("🚨 Com risco alto", int((filtrado["nivel_final"] == "alto").sum()))
    m3.metric("Avaliadas por você", int((filtrado["avaliacao"] != "sem avaliação").sum()))

    filtrado = filtrado.assign(risco=filtrado["nivel_final"].map(lambda n: NIVEIS[n]["rotulo"]))
    coluna = "tipo_golpe" if agrupar == "Tipo de golpe" else "canal"
    contagem = filtrado.groupby([coluna, "risco"]).size().reset_index(name="quantidade")

    fig = px.bar(
        contagem,
        x="quantidade",
        y=coluna,
        color="risco",
        orientation="h",
        text="quantidade",
        color_discrete_map=CORES_GRAFICO,
        category_orders={"risco": ["Risco alto", "Risco médio", "Risco baixo"]},
        labels={"quantidade": "Quantidade de mensagens", "tipo_golpe": "Tipo de golpe", "canal": "Canal", "risco": "Nível de risco"},
        title=f"Mensagens por {agrupar.lower()}",
    )
    fig.update_layout(yaxis_title="", xaxis_dtick=1, legend_title_text="Nível de risco")
    st.plotly_chart(fig, alt=f"Gráfico de barras com a quantidade de mensagens por {agrupar.lower()}, separadas por nível de risco.")

    st.markdown("**Lista das mensagens**")
    for _, linha in filtrado.sort_values("data", ascending=False).iterrows():
        detalhe = f"{linha['protocolo']} • {linha['canal']} • {linha['data']:%d/%m %H:%M} • avaliação: {linha['avaliacao']}"
        componentes.cartao_risco(linha["nivel_final"], linha["tipo_golpe"], detalhe, compacto=True)
