# Configurações do back-end. A chave vem do .env (que não vai pro GitHub)
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
# o gpt-6-luna aceita none, low, medium... deixe vazio se trocar para um modelo que não aceita esse campo
OPENAI_REASONING_EFFORT = os.getenv("OPENAI_REASONING_EFFORT", "low")
OPENAI_TIMEOUT = 25  # segundos

# origens que podem chamar a API pelo navegador (separadas por vírgula, nunca "*")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(",")

# avaliações dos cidadãos (sem o texto da mensagem)
ARQUIVO_FEEDBACK = os.path.join(os.path.dirname(__file__), "dados", "feedbacks.jsonl")
