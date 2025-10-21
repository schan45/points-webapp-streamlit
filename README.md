# Points → Score Calculator (Streamlit)

A tiny web app where users can input `(got, max)` rows and get the average normalized value and a 0–10 score.

## Run online (Streamlit Community Cloud)
1. Push this folder to a **public GitHub repo** (e.g., `USER/points-webapp-streamlit`).
2. Go to https://share.streamlit.io
   - Click **Deploy an app** → Connect your GitHub → select the repo
   - **App file**: `app.py`
3. After deploy, share the URL. Users can edit the table directly.

## Run online (Hugging Face Spaces)
1. Create a new **Space** → **Streamlit** template.
2. Upload these files (or connect to your GitHub).
3. Set `app.py` as the entry file.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features
- Editable table (add rows, paste from Excel)
- Validations (Max ≠ 0)
- Per-row normalized values
- Average and 0–10 score
- Rounding control
