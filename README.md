# AirLLM Browser Backend

Jednoduchý backend + web UI, aby sa AirLLM dalo ovládať z prehliadača bez práce v shelli.

## Ako to stiahnuť do svojho PC

### Možnosť A: Git (odporúčané)

```bash
git clone <URL_TVOJHO_REPA>
cd airllm-backend
```

> `<URL_TVOJHO_REPA>` nahraď URL adresou repozitára (napr. z GitHub/GitLabu).

### Možnosť B: ZIP archív

1. V repozitári klikni na **Code** → **Download ZIP**.
2. ZIP rozbaľ do priečinka na svojom PC.
3. Otvor terminál v rozbalenom priečinku `airllm-backend`.

## Čo to vie

- zobraziť stav AirLLM inštalácie
- načítať model cez API
- poslať prompt a dostať odpoveď
- používať cez jednoduché webové rozhranie na `/`

## Rýchly štart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# voliteľné, ak chceš reálnu inferenciu:
# pip install airllm
python -m app.main
```

Potom otvor:

- `http://localhost:8000`

## API endpointy

- `GET /api/status`
- `POST /api/load-model` body: `{ "model_name": "<hf-model>" }`
- `POST /api/generate` body: `{ "prompt": "...", "max_new_tokens": 128 }`

## Poznámka k AirLLM

Ak `airllm` nie je nainštalovaný, backend vráti vysvetlenie v status endpoint-e.
