Sample app to display stream response from ChatGPT API.

## Set up

```bash
cd server/python
cp .env.copy .env
```

Set `OPENAI_API_KEY`

## Launch app

### Server (Python, FastAPI)

```bash:
cd server/python

python3 -m venv .venv
(venv) pip install -r requirements.txt

(venv) python main.py
```

### Client (Next.js)

```bash
cd front
yarn install
yarn dev
```
