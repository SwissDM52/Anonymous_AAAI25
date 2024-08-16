from transformers import set_seed
from transformers import BloomTokenizerFast, BloomForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
import crypto
import datetime
import sys

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using CUDA device:", torch.cuda.get_device_name(0))
else:
    device = torch.device("cpu")
    print("CUDA is not available, using CPU.")

set_seed(1234)

model_name = "bloom_2b6"
tokenizer = BloomTokenizerFast.from_pretrained(model_name)
model = BloomForCausalLM.from_pretrained(model_name)
model.half()
model.eval()
model.to(device)


def EmbedAsymmetric(input_context, end, model, temperature=1.0, top_k=None, top_p=None, target_len=5, sentences=5):
    contexts = input_context
    output_words = []
    patter_s = re.compile(r'\s+')
    patter_n = re.compile(r'\n+')
    strdrs = ""
    while len(output_words) < target_len:
        context = tokenizer(contexts, return_tensors="pt").input_ids
        attention_mask = torch.ones_like(context)
        context = context.to(device)
        output = model.generate(
            context,
            temperature=temperature,
            max_new_tokens=target_len + 5,
            min_length=len(contexts) + 3,
            do_sample=True,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.eos_token_id,
            bos_token_id=tokenizer.bos_token_id,
            use_cache=True,
        )
        decoder = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
        if "�" in decoder:
            continue
        strd = decoder[len(input_context):]
        strd = re.sub(patter_n, ' ', strd)
        strd = re.sub(patter_s, ' ', strd)
        strd = strd.strip()
        if strd.count(' ') < target_len - 1:
            contexts = contexts + " " + strd
            continue
        spaces = [m.start() for m in re.finditer(r' ', strd)]
        if len(spaces) >= target_len:
            strdrs = strd[:spaces[target_len - 1]]
        strs = strdrs.split(" ")
        for i, text in enumerate(strs):
            if text == "":
                continue
            output_words.append(text)
            if len(output_words) == target_len:
                contexts = input_context + " " + strdrs
                break

    word = ''.join(output_words)
    return contexts, word, end, strdrs


def generate_text(input_context, generators, end):
    temperature = 1.05
    top_k = 30
    top_p = 0.85
    contexts, word, end, strdrs = EmbedAsymmetric(input_context, end, generators, temperature, top_k, top_p)
    return contexts, word, end, strdrs


def generate(input_context, model, l):
    words = []
    wordd = []
    strd = []
    wordss = []
    end = 0
    for i in range(4 * l * 2):
        context, word, ends, strdrs = generate_text(input_context, model, end)
        input_context = context
        print('{}\n{}\n{}\n'.format("==============================================================", word,
                                    input_context))
        words.append(word)
        wordss.append(word)
        strd.append(strdrs)
        wordd.append(word)
        # if end == 3:
        #     break
    #

    return input_context


def main():
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        l = int(sys.argv[2])
        print(f"Your keyword is: {input_text}")
    else:
        print("Please input your keyword and l.")
        return
    input_context = input_text
    now = datetime.datetime.now()
    for i in range(1):
        output_context = generate(input_context, model, l)
    now2 = datetime.datetime.now()
    print("The average duration over 1 times is：", (now2 - now) / 1)


if __name__ == "__main__":
    main()
