from transformers import pipeline, set_seed
from transformers import BloomTokenizerFast, BloomForCausalLM
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
            max_new_tokens=target_len+5,
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
        if strd.count(' ')<target_len-1:
            contexts = contexts+" "+strd
            continue
        spaces = [m.start() for m in re.finditer(r' ', strd)]
        if len(spaces) >= target_len:
            strdrs = strd[:spaces[target_len-1]]
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


def generate(pairing, g1, g, p, input_context, model, users, userr1, userr2, l):
    σ = crypto.sign_mdvs(pairing, input_context, users[0], users[1], [userr1[1], userr2[1]], g)
    x1 = crypto.hex_to_binary(str(σ[0])).zfill(l)
    x2 = crypto.hex_to_binary(str(σ[1])).zfill(l)
    x3 = crypto.hex_to_binary(str(σ[2])).zfill(l)
    x4 = crypto.hex_to_binary(str(σ[3])).zfill(l)
    s = x1 + x2 + x3 + x4
    ss = list(s)
    n = 0
    words = []
    wordd = []
    strd = []
    wordss = []
    end = 0
    for i in range(4*l*2):
        # char = ss[len(ss) - l]
        char = ss[i]
        while True:
            # word = generate_text(input_context, generator)
            context, word, ends, strdrs = generate_text(input_context, model, end)
            hs = crypto.hash_one_word(word)
            print("char == {}, hs == {}, word == {}, i == {}".format(char, hs, word, i))
            if hs == char:
                break
            if end == 3:
                break
        input_context = context
        words.append(word)
        wordss.append(word)
        strd.append(strdrs)
        wordd.append(word)
        n += 1
        if n == l * 4:
            m1 = "".join(words)
            σ1 = crypto.sign_mdvs(pairing, m1, users[0], users[1], [userr1[1], userr2[1]], g)
            xx1 = crypto.hex_to_binary(str(σ1[0])).zfill(l)
            xx2 = crypto.hex_to_binary(str(σ1[1])).zfill(l)
            xx3 = crypto.hex_to_binary(str(σ1[2])).zfill(l)
            xx4 = crypto.hex_to_binary(str(σ1[3])).zfill(l)
            print(xx1,xx2,xx3,xx4)
            s1 = xx1 + xx2 + xx3 + xx4
            ss.extend(s1)
            words = []
            n = 0
        if end == 3:
            break

    #print(''.join(ss))
    return input_context, strd, wordss


def verify(pairing, input_context, output_context, g, pks, pkr1, pkr2, l, p, strd, wordss, target_len=5):
    output = output_context[len(input_context):]
    output = output.strip()

    strs = []
    strsd = output.split(" ")

    for i in range(0, len(strsd), target_len):
        if i + target_len - 1 < len(strsd):
            strs.append(''.join(strsd[i:i + target_len]))

    m1 = "".join(strs[0:l * 4])
    m2 = strs[l * 4:l * 4 * 2]
    s = ""
    for i in range(len(m2)):
        hs = crypto.hash_one_word(m2[i])
        s = s + hs
    #print(s)

    for i in range(len(strs)):
        print("[{}]".format(strd[i]))
        print("{} {} {}".format(strs[i], wordss[i], strs[i] == wordss[i]))

    print(output)

    m1 = m1
    c1 = int(s[0:l], 2)
    c2 = int(s[l:l * 2], 2)
    z1 = int(s[l * 2:l * 3], 2)
    z2 = int(s[l * 3:l * 4], 2)
    #print(s[0:l],s[l:l*2],s[l*2:l*3],s[l*3:l*4])
    print("The verify result is：", crypto.verify_mdvs(pairing, m1, pks, c1, c2, z1, z2, [pkr1, pkr2], g))


def main():
    function_map = {
        8: crypto.setup_8,
        16: crypto.setup_16,
        24: crypto.setup_24,
        32: crypto.setup_32,
        40: crypto.setup_40,
        48: crypto.setup_48,
    }
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        l = int(sys.argv[2])
        print(f"Your keyword is: {input_text}")
    else:
        print("Please input your keyword and l.")
        return
    input_context = input_text
    params, pairing, g1, g, p = function_map[l]()
    users = crypto.kg_mdvs(pairing, g)
    #print(users)
    userr1 = crypto.kg_mdvs(pairing, g)
    userr2 = crypto.kg_mdvs(pairing, g)
    now = datetime.datetime.now()
    now3 = []
    for i in range(1):
        output_context, strd, wordss = generate(pairing, g1, g, p, input_context, model, users, userr1, userr2, l)
        now1 = datetime.datetime.now()
        verify(pairing, input_context, output_context, g, users[1], userr1[1], userr2[1], l, p, strd, wordss)
        now2 = datetime.datetime.now()
        #now3.append(now2-now)
    #now2 = datetime.datetime.now()
    print("The average duration over 1 times is：", (now1 - now) / 1)
    print("The verification time is：",now2-now1)
    # verify(pairing, input_context, output_context, g, users[1], userr1[1], userr2[1], l, p, strd, wordss)


if __name__ == "__main__":
    main()

