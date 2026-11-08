# Parte 1 – Questão 2: API de tradução EN → FR (FastAPI + HuggingFace)

API que traduz textos do inglês para o francês com o modelo **Helsinki-NLP/opus-mt-en-fr** (MarianMT), via `transformers`.

## Estrutura

```
parte1-q2-fastapi-traducao-en-fr/
├── app/
│   ├── __init__.py
│   ├── main.py        # aplicação FastAPI + carga do modelo
│   └── schemas.py     # modelos Pydantic
├── tests/
│   └── test_api.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

O modelo (~300 MB) é baixado na primeira execução. Documentação interativa: http://127.0.0.1:8000/docs

## Exemplo de uso

```bash
curl -X POST http://127.0.0.1:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you? I hope you are well."}'
```

Resposta:

```json
{
  "original_text": "Hello, how are you? I hope you are well.",
  "translated_text": "Bonjour, comment allez-vous ? J'espère que vous allez bien.",
  "source_language": "en",
  "target_language": "fr",
  "model": "Helsinki-NLP/opus-mt-en-fr"
}
```

## Textos curtos e longos

Textos longos são divididos em sentenças (`.`, `!`, `?`), traduzidos em lote e reunidos novamente, respeitando o limite de tokens do modelo.

## Testes

```bash
pytest -q
```
