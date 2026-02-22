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


## Riešenie chyby ERR_ADDRESS_INVALID

Ak si skopíroval adresu `http://0.0.0.0:8000`, prehliadač ju často odmietne (`ERR_ADDRESS_INVALID`).

Použi jednu z týchto adries:

- `http://localhost:8000`
- `http://127.0.0.1:8000`

`0.0.0.0` je bind adresa servera (načúva na všetkých rozhraniach), ale nie je to adresa určená na otvorenie v prehliadači.

Ak stále stránka nejde:

1. skontroluj, či server beží (`python -m app.main`)
2. skontroluj, či port 8000 nie je obsadený
3. na inom zariadení v sieti použi IP adresu počítača, napr. `http://192.168.1.25:8000`


## Chyba: `No module named 'optimum.bettertransformer'`

Táto chyba znamená, že AirLLM je nainštalované, ale verzia závislosti `optimum` je nekompatibilná.

Riešenie vo virtuálnom prostredí:

```bash
pip install --upgrade --force-reinstall "optimum<2" airllm
```

Potom reštartuj backend:

```bash
python -m app.main
```

Ak používaš čisté prostredie, odporúčaný postup je: vytvoriť nové venv, nainštalovať závislosti a až potom AirLLM.

## GitHub repo neodráža zmeny?

Ak nevidíš nové commity na GitHube, zmeny sú pravdepodobne len lokálne.

Skontroluj remote:

```bash
git remote -v
```

Ak je výstup prázdny, nastav remote:

```bash
git remote add origin <URL_TVOJHO_REPA>
```

Potom pushni vetvu:

```bash
git push -u origin work
```

Ak používaš inú vetvu, nahraď `work` názvom svojej vetvy (zistíš cez `git branch --show-current`).

Pri pushi ťa môže GitHub vyzvať na autentifikáciu (PAT token alebo SSH kľúč).

## API endpointy

- `GET /api/status`
- `POST /api/load-model` body: `{ "model_name": "<hf-model>" }`
- `POST /api/generate` body: `{ "prompt": "...", "max_new_tokens": 128 }`

## Poznámka k AirLLM

Ak `airllm` nie je nainštalovaný, backend vráti vysvetlenie v status endpoint-e.
