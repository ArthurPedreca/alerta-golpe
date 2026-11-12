# Única parte do back-end que fala com a OpenAI
import logging

from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError
from pydantic import ValidationError

import config
from schemas.analise import AnaliseIA

log = logging.getLogger("llm_provider")


class ErroIA(Exception):
    pass


class TimeoutIA(ErroIA):
    pass


class RespostaInvalidaIA(ErroIA):
    pass


_cliente = None


def _pegar_cliente():
    global _cliente
    if not config.OPENAI_API_KEY:
        raise ErroIA("OPENAI_API_KEY não configurada no .env")
    if _cliente is None:
        _cliente = OpenAI(api_key=config.OPENAI_API_KEY, timeout=config.OPENAI_TIMEOUT, max_retries=0)
    return _cliente


def gerar_analise(prompt_sistema, prompt_usuario):
    cliente = _pegar_cliente()

    extras = {}
    if config.OPENAI_REASONING_EFFORT:
        extras["reasoning_effort"] = config.OPENAI_REASONING_EFFORT

    try:
        # parse() manda o schema do Pydantic e já devolve o objeto validado
        resposta = cliente.chat.completions.parse(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            response_format=AnaliseIA,
            **extras,
        )
    except APITimeoutError as erro:
        log.warning("timeout na OpenAI: %s", erro)
        raise TimeoutIA("a IA demorou demais") from erro
    except APIConnectionError as erro:
        log.warning("sem conexão com a OpenAI: %s", erro)
        raise ErroIA("sem conexão com a IA") from erro
    except ValidationError as erro:
        log.warning("IA devolveu JSON fora do formato: %s", erro)
        raise RespostaInvalidaIA("resposta fora do formato") from erro
    except OpenAIError as erro:
        # chave errada, sem crédito, modelo inexistente etc. (não loga a mensagem do cidadão)
        log.warning("erro da OpenAI: %s", type(erro).__name__)
        raise ErroIA("erro na IA") from erro

    mensagem = resposta.choices[0].message
    if mensagem.refusal or mensagem.parsed is None:
        log.warning("IA recusou ou não devolveu o objeto")
        raise RespostaInvalidaIA("resposta vazia")

    return mensagem.parsed
