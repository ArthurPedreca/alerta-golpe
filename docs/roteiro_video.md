# Roteiro do vídeo (até 5 minutos)

Antes de gravar: `docker compose up --build`, abrir http://localhost:8501 em uma aba e o VS Code em outra janela. Deixar o histórico vazio.

Sugestão de divisão: um integrante apresenta as partes 1 e 2 (problema e demonstração) e o outro as partes 3 e 4 (código e validação).

## 1. Problema, público e ODS (0:00 a 0:45)

**Tela:** README, seção 1 e 7.1.

> Esse é o Alerta Golpe. Em 2025 o Brasil teve mais de 2,2 milhões de estelionatos, 258 por hora, e 1 em cada 4 brasileiros perdeu dinheiro com golpe digital. O app é para a pessoa que recebe uma mensagem estranha e não tem para quem perguntar antes de fazer o Pix. Ele se relaciona com o ODS 16, porque ajuda a prevenir um crime que quase nunca é punido, e com o ODS 10, porque metade das vítimas ganha até 2 salários mínimos.

## 2. Demonstração (0:45 a 2:30)

1. Clicar em **Verificar mensagem** com tudo vazio → aparecem os avisos de validação.
2. Colar a mensagem do falso parente, escolher WhatsApp e "Sim" → mostrar o **spinner** enquanto a IA responde.
3. Mostrar o **cartão de risco** (cor + ícone + texto), sinais de alerta, o que fazer e onde pedir ajuda.
4. **Human-in-the-loop:** marcar "Está errada", escolher outro nível e enviar → mostrar a mensagem de obrigado.
5. Verificar a mensagem do condomínio.
6. Mandar a mesma mensagem de novo → mostrar o aviso de que veio do cache e não chamou a IA.
7. Aba **Meu histórico:** mostrar o gráfico (passar o mouse e dar zoom), mudar os filtros de nível e canal e trocar "Ver o gráfico por".
8. **Cenário de erro:** no terminal rodar `docker compose stop api`, tentar verificar uma mensagem → mensagem amigável e barra lateral vermelha. Depois `docker compose start api`.

## 3. Código (2:30 a 4:00)

1. Mostrar as pastas `frontend/` (features, ui, state, providers) e `backend/` (routers, schemas, pipelines, providers).
2. `backend/providers/llm_provider.py` → **onde a IA é chamada**: `chat.completions.parse` com `response_format=AnaliseIA`.
3. `backend/schemas/analise.py` → o modelo Pydantic com os `Literal` de nível e tipo.
4. `backend/pipelines/analise_golpe.py` → máscara de dados pessoais, prompt e a regra de segurança.
5. `frontend/state/sessao.py` → **estado** (histórico no `st.session_state`).
6. `frontend/providers/api_cliente.py` → **cache** (`@st.cache_data` e `@st.cache_resource`) e tratamento de erro.
7. **Chave da API:** `.env.example`, `.gitignore` com `.env` e `config.py` lendo a variável. Mostrar o `CORSMiddleware` no `main.py`.

## 4. Validação (4:00 a 4:50)

1. Mostrar a tabela dos casos de teste da IA no README e falar o que não bateu e o ajuste feito.
2. Mostrar a tabela do teste com as 3 pessoas e o ajuste feito a partir do que elas falaram (antes e depois na tela).

## 5. Fechamento (4:50 a 5:00)

> A IA não substitui o banco nem a polícia, mas ajuda a pessoa a parar e desconfiar antes de pagar. Obrigado.
