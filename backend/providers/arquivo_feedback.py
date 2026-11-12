# Guarda as avaliações dos cidadãos num arquivo .jsonl (uma linha por avaliação)
# Não guarda o texto da mensagem, só o protocolo e o que a pessoa achou
import json
import os
from datetime import datetime

import config


def salvar(dados):
    os.makedirs(os.path.dirname(config.ARQUIVO_FEEDBACK), exist_ok=True)
    dados["salvo_em"] = datetime.now().isoformat(timespec="seconds")
    with open(config.ARQUIVO_FEEDBACK, "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(dados, ensure_ascii=False) + "\n")
