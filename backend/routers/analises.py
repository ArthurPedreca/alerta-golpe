# Rotas da API
from fastapi import APIRouter, HTTPException

from pipelines import analise_golpe
from providers import arquivo_feedback
from providers.llm_provider import ErroIA, RespostaInvalidaIA, TimeoutIA
from schemas.analise import Feedback, PedidoAnalise, RespostaAnalise

router = APIRouter(prefix="/v1", tags=["análises"])


@router.post("/analises", response_model=RespostaAnalise)
def criar_analise(pedido: PedidoAnalise):
    try:
        return analise_golpe.analisar(pedido)
    except TimeoutIA:
        raise HTTPException(status_code=504, detail="A IA demorou demais para responder")
    except RespostaInvalidaIA:
        raise HTTPException(status_code=502, detail="A IA devolveu uma resposta fora do formato")
    except ErroIA:
        raise HTTPException(status_code=503, detail="Serviço de IA indisponível no momento")


@router.post("/feedback", status_code=201)
def salvar_feedback(feedback: Feedback):
    dados = feedback.model_dump()
    if dados["comentario"]:
        dados["comentario"] = analise_golpe.mascarar_dados_pessoais(dados["comentario"])
    arquivo_feedback.salvar(dados)
    return {"ok": True}


@router.get("/tipos-golpe")
def listar_tipos_golpe():
    return [{"tipo": tipo, "descricao": desc} for tipo, desc in analise_golpe.DESCRICAO_TIPOS.items()]
