# Roda os casos de teste da IA na API e monta a tabela para o README
# Precisa da API rodando (uvicorn ou docker compose up)
# Uso: python testes_ia/rodar_casos.py
import os
import sys

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

# mensagens de teste escritas por nós, imitando golpes comuns (não são mensagens reais de ninguém)
CASOS = [
    {
        "nome": "Falso parente",
        "mensagem": "Oi mãe, troquei de número, salva esse. Meu app do banco travou e preciso pagar um boleto hoje. Consegue me fazer um Pix de R$ 850? Amanhã te devolvo.",
        "canal": "WhatsApp",
        "pede_dinheiro": "sim",
        "esperado_nivel": "alto",
        "esperado_tipo": "Falso parente ou amigo",
    },
    {
        "nome": "Taxa de entrega",
        "mensagem": "CORREIOS: Sua encomenda está retida por falta de pagamento da taxa de R$ 12,90. Regularize em até 24h para não ser devolvida: http://correios-rastreio-entrega.com/pagar",
        "canal": "SMS",
        "pede_dinheiro": "nao_sei",
        "esperado_nivel": "alto",
        "esperado_tipo": "Falsa entrega ou taxa",
    },
    {
        "nome": "Falsa central",
        "mensagem": "Aqui é da central de segurança do seu banco. Identificamos uma compra de R$ 2.399 no seu cartão. Se não reconhece, informe o código que vai chegar por SMS para cancelarmos.",
        "canal": "Ligação",
        "pede_dinheiro": "sim",
        "esperado_nivel": "alto",
        "esperado_tipo": "Falsa central do banco",
    },
    {
        "nome": "Mensagem normal",
        "mensagem": "Oi pessoal, a reunião do condomínio foi remarcada para quinta às 19h no salão de festas. Qualquer dúvida me chama.",
        "canal": "WhatsApp",
        "pede_dinheiro": "nao",
        "esperado_nivel": "baixo",
        "esperado_tipo": "Não parece golpe",
    },
    {
        "nome": "Vaga com taxa",
        "mensagem": "Vaga home office! Ganhe R$ 300 por dia só curtindo vídeos. Para começar é só pagar a taxa de cadastro de R$ 49 no Pix.",
        "canal": "Rede social",
        "pede_dinheiro": "sim",
        "esperado_nivel": "alto",
        "esperado_tipo": "Falsa vaga de emprego",
    },
]


def main():
    linhas = ["| # | Entrada | Saída esperada | Saída obtida | Bateu? | Ajuste realizado |", "|---|---|---|---|---|---|"]
    for i, caso in enumerate(CASOS, start=1):
        print(f"[{i}/{len(CASOS)}] {caso['nome']}...")
        try:
            r = requests.post(f"{API_URL}/v1/analises", json={
                "mensagem": caso["mensagem"], "canal": caso["canal"], "pede_dinheiro": caso["pede_dinheiro"],
            }, timeout=60)
            r.raise_for_status()
            analise = r.json()["analise"]
            obtido = f"{analise['nivel_risco']} / {analise['tipo_golpe']}"
            bateu = "sim" if analise["nivel_risco"] == caso["esperado_nivel"] and analise["tipo_golpe"] == caso["esperado_tipo"] else "não"
            print("   resumo da IA:", analise["resumo"])
        except requests.RequestException as erro:
            obtido = f"erro: {erro}"
            bateu = "não"
        entrada = f"{caso['nome']} ({caso['canal']}): \"{caso['mensagem'][:70]}...\""
        esperado = f"{caso['esperado_nivel']} / {caso['esperado_tipo']}"
        linhas.append(f"| {i} | {entrada} | {esperado} | {obtido} | {bateu} | |")

    tabela = "\n".join(linhas)
    print("\n" + tabela)
    saida = os.path.join(os.path.dirname(__file__), "resultado_casos.md")
    with open(saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(tabela + "\n")
    print(f"\nTabela salva em {saida}. Preencha a coluna 'Ajuste realizado' e cole no README.")


if __name__ == "__main__":
    sys.exit(main())
