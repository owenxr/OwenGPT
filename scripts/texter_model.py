# all the imports
import random
import logging
import torch
import threading
from transformers import (
    MODEL_WITH_LM_HEAD_MAPPING,
    AutoTokenizer,
    GPT2LMHeadModel
)

# HUGGING FACE API KEY
API_KEY = ""
with open('params/API_KEY.txt', 'r') as api_key_file:
    API_KEY = api_key_file.readline()

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
model = GPT2LMHeadModel.from_pretrained("MODEL_NAME", token=API_KEY)


def pre_text_gen(pretext):

    if len(pretext) == 0:
        print("No Pretext Found")
        return False, None

    app_text = tokenizer.bos_token
    for text in pretext:
        curr_text = text
        app_text += curr_text

    app_text += tokenizer.eos_token
    new_user_input_ids = tokenizer.encode(app_text, return_tensors='pt')

    return True, new_user_input_ids


def gen_responses(pretext):
    toggle, new_user_input_ids = pre_text_gen(pretext)

    responses = []

    step = 0

    for _ in range(random.randint(1, 2)):
        bot_input_ids = torch.cat(
            [chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        step += 1

        # generated a response while limiting the total chat history to 1000 tokens,
        chat_history_ids = model.generate(
            bot_input_ids, max_new_tokens=500,
            min_new_tokens=6,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            repetition_penalty=0.8,
            do_sample=True,
            top_k=75,
            top_p=0.6,
            temperature=0.8
        )

        # pretty print last ouput tokens from bot
        responses.append(("{}".format(tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))))

    return responses
