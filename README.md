# Quick 3–5 Sentence Summary

This repo contains a FastAPI backend plus a Chrome extension that summarize long text into 3–5 sentence summaries using `facebook/bart-large-cnn`.

## 1. Setup and run the backend
1. Download/Clone the repo
2. From the repo root:
```bash
pip install fastapi "uvicorn[standard]" torch transformers
uvicorn api:app --reload
```
The API will be available at http://localhost:8000/summarize

- Request body: {"text": "your article text"}
- Response: {"summary": "3–5 sentence summary"}

## 2. Load the Chrome extension

1. Open Chrome and go to chrome://extensions.
2. Turn on Developer mode.
3. Click Load unpacked.
4. Select the summary-extension folder in this repo.
5. The extension is preconfigured to call http://localhost:8000/summarize.

## 3. Use the extension
1. Make sure the backend (uvicorn api:app --reload) is running.
2. Open any article in Chrome.
3. Highlight the text you want summarized.
4. Click the extension icon and then Summarize.
5. A 3–5 sentence summary appears in the popup.
