
- `GET /projects`: Zwraca listę projektów ustawodawczych.
- `GET /project/{project_id}`: Zwraca szczegóły konkretnego projektu, włącznie z etapami.
- `GET /project/{project_id}/stage/{katalog_id}`: Zwraca dokumenty dla konkretnego etapu.

 Python 3.11+
 Zainstaluj zależności: `pip install -r requirements.txt`
 Uruchom serwer: `uvicorn main:app`

dokumentacja na  http://127.0.0.1:8000/docs po uruchomieniu serwera