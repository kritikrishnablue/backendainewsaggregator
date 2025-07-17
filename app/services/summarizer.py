from transformers.pipelines import pipeline
from typing import Optional

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_length: int = 130, min_length: int = 30) -> Optional[str]:
    if not text or len(text) < 30:
        return None
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print("❌ Summarization error:", e)
        return None
