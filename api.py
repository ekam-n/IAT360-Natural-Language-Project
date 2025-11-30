from fastapi import FastAPI
from pydantic import BaseModel
import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model and tokenizer once
MODEL_NAME = "facebook/bart-large-cnn"
device = "cuda:0" if torch.cuda.is_available() else "cpu"

tok = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
).to(device)
model.eval()

# Reuse your 3–5 sentence helper here
import re
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

def keep_3_to_5_sentences(text, min_sents=3, max_sents=5):
  sents = [s.strip() for s in _SENT_SPLIT_RE.split(text.strip()) if s.strip()]
  if len(sents) <= max_sents:
    return " ".join(sents)
  return " ".join(sents[:max_sents])

def summarize_safe(text, max_new=160, min_new=80):
  enc = tok(
      text,
      truncation=True,
      max_length=1024,
      return_tensors="pt"
  ).to(device)
  with torch.inference_mode():
    out = model.generate(
        **enc,
        max_new_tokens=max_new,
        min_new_tokens=min_new,
        num_beams=4,
        length_penalty=1.0,
        early_stopping=True
    )
  raw = tok.batch_decode(out, skip_special_tokens=True)[0].strip()
  return keep_3_to_5_sentences(raw)

app = FastAPI()

class SummarizeRequest(BaseModel):
  text: str

class SummarizeResponse(BaseModel):
  summary: str

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
  summary = summarize_safe(req.text)
  return SummarizeResponse(summary=summary)
