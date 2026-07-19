from transformers import AutoModelForCausalLM, AutoTokenizer
from app.core.config import settings


_tokenizer: AutoTokenizer | None = None
_model: AutoModelForCausalLM | None = None


def initialize():
    global _model, _tokenizer
    if _model is None:
        _model = AutoModelForCausalLM.from_pretrained(
            settings.model_name, torch_dtype="auto", device_map="auto"
        )
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(settings.model_name)


def get_tokenizer():
    global _tokenizer
    return _tokenizer


def get_model():
    global _model
    return _model
