# Modelos Pydantic de entrada e saída da API
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

Canal = Literal["WhatsApp", "SMS", "E-mail", "Ligação", "Rede social", "Outro"]
NivelRisco = Literal["baixo", "medio", "alto"]
PedeDinheiro = Literal["sim", "nao", "nao_sei"]

# lista fechada pra IA não inventar categoria (e pro front conseguir fazer gráfico)
TipoGolpe = Literal[
    "Falso parente ou amigo",
    "Falsa central do banco",
    "Falsa entrega ou taxa",
    "Link falso para roubar dados",
    "Falso prêmio ou promoção",
    "Falsa vaga de emprego",
    "Falso boleto ou cobrança",
    "Investimento milagroso",
    "Outro tipo de golpe",
    "Não parece golpe",
]


class PedidoAnalise(BaseModel):
    mensagem: str = Field(min_length=10, max_length=2000)
    canal: Canal
    pede_dinheiro: PedeDinheiro = "nao_sei"

    @field_validator("mensagem")
    @classmethod
    def limpar_mensagem(cls, valor):
        valor = valor.strip()
        if len(valor) < 10:
            raise ValueError("a mensagem precisa ter pelo menos 10 caracteres")
        return valor


class AnaliseIA(BaseModel):
    """Formato que a IA é obrigada a devolver (saída estruturada)"""

    nivel_risco: NivelRisco
    tipo_golpe: TipoGolpe
    resumo: str
    sinais_alerta: list[str]
    o_que_fazer: list[str]


class RespostaAnalise(BaseModel):
    protocolo: str
    criado_em: datetime
    canal: Canal
    analise: AnaliseIA
    ajustado_pela_regra: bool = False  # True quando a regra de segurança subiu o nível
    onde_pedir_ajuda: list[str]


class Feedback(BaseModel):
    protocolo: str = Field(min_length=5, max_length=40)
    nivel_ia: NivelRisco
    util: bool
    nivel_correto: Optional[NivelRisco] = None
    comentario: Optional[str] = Field(default=None, max_length=300)
