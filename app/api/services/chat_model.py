from threading import Thread

from transformers import TextIteratorStreamer

from app.api.services.bootstrap import get_model, get_tokenizer

_SYSTEM_PROMPT = (
    "You are Qwen, created by Alibaba Cloud. "
    "You are a helpful assistant."
)


def _prepare_inputs(prompt: str):
    tokenizer = get_tokenizer()
    model = get_model()

    messages = [
        {
            "role": "system",
            "content": _SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    chat_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        chat_prompt,
        return_tensors="pt",
    ).to(model.device)

    return tokenizer, model, inputs


def generate_text(prompt: str, max_new_tokens: int = 512) -> str:
    tokenizer, model, inputs = _prepare_inputs(prompt)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
    )

    generated_tokens = outputs[:, inputs.input_ids.shape[1]:]

    return tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
    )[0]


def generate_stream(prompt: str, max_new_tokens: int = 512):
    tokenizer, model, inputs = _prepare_inputs(prompt)

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True,
    )

    thread = Thread(
        target=model.generate,
        kwargs={
            **inputs,
            "streamer": streamer,
            "max_new_tokens": max_new_tokens,
        },
    )

    thread.start()

    yield from streamer