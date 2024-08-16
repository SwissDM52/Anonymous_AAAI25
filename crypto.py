from pypbc import *
import hashlib
from Cryptodome.Util.number import bytes_to_long

stored_params = """type a
q 15321664075303276999488783323815870836986283575270518373346977914323998507816373271572862490476122028315228441173950368532612993832753284289504842010535559
h 10483507978331640839926094555207443546343363992240932672311782266534699429550735889668503320752981377603960
r 1461501637330902918203607461463827683388751347711
exp2 160
exp1 86
sign1 -1
sign0 -1
"""
g1s = "03007CE73CD5FCBBABA85BC10F66C83D901F7DA8AF46E9049907012BE1521B5C876B71E63E0AAD8067237DCAC1026ECA1BCFEFA69C4B4651F557BC882F8860250133"
g2s = "02007A5E3D81F8ACC91535256768D8E29E5964C99242EB67B589EEF655D9BA8613B5B2804109959C091222288542F272646596D82D1DBFFE4B39B5BF6DE0A41B5A3E"

stored_params_128 = """type a
q 336400065263281888719487864915889308859
h 265372860
r 1267650600228229400397191577601
exp2 100
exp1 40
sign1 -1
sign0 1
"""
g1_128 = "0269DC6B57BF4903CF6607D2DEC61B512C"
g2_128 = "02A835E2720EC536ED2B57CABDFD73BE0D"

g1_10 = "020F5C4187"
g2_10 = "02070E8B05"

stored_params_48 = """type a
q 186806049823049799178034957910489980867
h 663669674338485264162876
r 281474439839743
exp2 48
exp1 29
sign1 -1
sign0 -1
"""
g1_48 = "0386107C40EF6B47324ECF0363023D7513"
g2_48 = "028C6FA350D17B466FFEF0C7B935AE172A"

stored_params_40 = """type a
q 288210961026028841557127940766484542271
h 349501789395166686331653312
r 824633720831
exp2 40
exp1 38
sign1 -1
sign0 -1
"""
g1_40 = "030E42E14B7871F3D75BD7E24FD5A8A581"
g2_40 = "020105BAAFAE04DDAD12EC8D50F3FF382F"

stored_params_32 = """type a
q 315721326357650336423152999616492907251
h 73509599922065049199913357388
r 4294967279
exp2 32
exp1 4
sign1 -1
sign0 -1
"""
g1_32 = "03C75E5E7C48FC909B555C0F28BF94FCEF"
g2_32 = "0370D06E73DB5C0B6B1C9C84D0FC0A6E27"

stored_params_24 = """type a
q 16137892151105269309422819024617620871
h 961893501090155397646964309544
r 16777213
exp2 24
exp1 2
sign1 -1
sign0 1
"""
g1_24 = "02049ADF116004C02736DEDBA81B536A87"
g2_24 = "0302AD7AB643468545544F31F07DABA55B"

stored_params_16 = """type a
q 505920891637755122030645756327006180363
h 7721743183469758726944027783192756
r 65519
exp2 16
exp1 4
sign1 -1
sign0 -1
"""
g1_16 = "020061452798BC58489554890022AABB7CD0"
g2_16 = "02013EA466DC1D2236D604705FC072312D9A"

stored_params_8 = """type a
q 193490726677733595723278478087316211147
h 1002542625273231065923722684390239436
r 193
exp2 8
exp1 6
sign1 -1
sign0 1
"""
g1_8 = "0332DED3DC5FE4AC5F5D73E4688E8B1ADD"
g2_8 = "0356C0AC1C6C5EF414635E32ED6343D253"


def hash0(pairing, g, p, m, r):
    mr = m + r
    if isinstance(mr, str):
        mr = mr.encode('utf-8')
    hash_object = hashlib.sha256(mr)
    hash_binary = hash_object.digest()
    # decimal_value = int.from_bytes(hash_binary, byteorder='big')
    h1x = bytes_to_long(hash_binary)
    if h1x >= p:
        h1x %= p
    h1x_element = Element(pairing, Zr, value=h1x)
    h = g * h1x_element
    return h


def hash(pairing, g, p, m):
    if isinstance(m, str):
        m = m.encode('utf-8')
    hash_object = hashlib.sha256(m)
    hash_binary = hash_object.digest()
    # decimal_value = int.from_bytes(hash_binary, byteorder='big')
    h1x = bytes_to_long(hash_binary)
    if h1x >= p:
        h1x %= p
    h1x_element = Element(pairing, Zr, value=h1x)
    h = g * h1x_element
    return h


def hash1(data, l):
    if isinstance(data, int):
        data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
    elif not isinstance(data, (bytes, bytearray)):
        data = str(data).encode('utf-8')
    hash_object = hashlib.sha256(data)
    hash_hex = hash_object.hexdigest()
    binary_string = ''.join(f"{int(hex_digit, 16):04b}" for hex_digit in hash_hex)
    binary_string = binary_string[-l:]
    return binary_string


def hash_bls(data, l):
    if isinstance(data, int):
        data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
    elif not isinstance(data, (bytes, bytearray)):
        data = str(data).encode('utf-8')
    hash_object = hashlib.sha256(data)
    hash_hex = hash_object.hexdigest()
    binary_string = ''.join(f"{int(hex_digit, 16):04b}" for hex_digit in hash_hex)
    binary_string = binary_string[-l:]
    return binary_string


def hash_mdvs_bin(data):
    # data = ""
    # for i in range(len(datas)):
    #     data = "{}{}".format(data, datas[i])
    # data = "{}{}{}{}".format(pks, pk, m, i)
    if isinstance(data, int):
        data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
    elif not isinstance(data, (bytes, bytearray)):
        data = str(data).encode('utf-8')
    hash_object = hashlib.sha256(data)
    hash_hex = hash_object.hexdigest()
    binary_string = ''.join(f"{int(hex_digit, 16):04b}" for hex_digit in hash_hex)
    # binary_string = binary_string[-l:]

    return binary_string


def hash_mdvs(datas):
    data = "".join(map(str, datas))
    if isinstance(data, int):
        data = data.to_bytes((data.bit_length() + 7) // 8, 'big')
    else:
        data = str(data).encode('utf-8')
    hash_object = hashlib.sha256(data)
    hash_hex = hash_object.hexdigest()
    hash_decimal = int(hash_hex, 16)
    return hash_decimal


def hash_enc(data):
    if isinstance(data, int):
        data = data.to_bytes((data.bit_length() + 7) // 8, 'big')  
    else:
        data = str(data).encode('utf-8')
    sha512 = hashlib.sha512()
    sha512.update(data)
    hex_digest = sha512.hexdigest()

    binary_digest = bin(int(hex_digest, 16))[2:].zfill(512)
    return binary_digest


def hashs(m):
    if isinstance(m, str):
        m = m.encode('utf-8')
    hash_object = hashlib.sha256(m)
    hash_hex = hash_object.hexdigest()
    binary_string = ''.join(f"{int(hex_digit, 16):04b}" for hex_digit in hash_hex)
    return binary_string


def hash_one_word(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    hash_object = hashlib.sha256(data)
    hash_hex = hash_object.hexdigest()
    binary_string = ''.join(f"{int(hex_digit, 16):04b}" for hex_digit in hash_hex)
    binary_string = binary_string[-1:]
    return binary_string


def setup_random():
    params = Parameters(qbits=128, rbits=12)
    pairing = Pairing(params)
    g = Element.random(pairing, G2)
    g1 = Element.random(pairing, G1)
    print(params)
    print("g1 = ", g1)
    print("g = ", g)


def setup():
    params = Parameters(param_string=stored_params)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2s)
    g1 = Element(pairing, G1, value=g1s)
    p = 15321664075303276999488783323815870836986283575270518373346977914323998507816373271572862490476122028315228441173950368532612993832753284289504842010535559
    # print(params)
    return params, pairing, g1, g, p


def setup_128():
    params = Parameters(param_string=stored_params_128)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2_128)
    g1 = Element(pairing, G1, value=g1_128)

    p = 336400065263281888719487864915889308859
    # print(params)
    return params, pairing, g1, g, p


def setup_48():
    params = Parameters(param_string=stored_params_48)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2_48)
    g1 = Element(pairing, G1, value=g1_48)

    p = 186806049823049799178034957910489980867
    # print(params)
    return params, pairing, g1, g, p


def setup_40():
    params = Parameters(param_string=stored_params_40)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2_40)
    g1 = Element(pairing, G1, value=g1_40)

    p = 288210961026028841557127940766484542271
    # print(params)
    return params, pairing, g1, g, p


def setup_32():
    params = Parameters(param_string=stored_params_32)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2_32)
    g1 = Element(pairing, G1, value=g1_32)

    p = 315721326357650336423152999616492907251
    # print(params)
    return params, pairing, g1, g, p


def setup_24():
    params = Parameters(param_string=stored_params_24)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2_24)
    g1 = Element(pairing, G1, value=g1_24)

    p = 16137892151105269309422819024617620871
    # print(params)
    return params, pairing, g1, g, p


def setup_16():
    params = Parameters(param_string=stored_params_16)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2_16)
    g1 = Element(pairing, G1, value=g1_16)

    p = 505920891637755122030645756327006180363
    # print(params)
    return params, pairing, g1, g, p


def setup_8():
    params = Parameters(param_string=stored_params_8)
    pairing = Pairing(params)

    g = Element(pairing, G2, value=g2_8)
    g1 = Element(pairing, G1, value=g1_8)

    p = 193490726677733595723278478087316211147
    # print(params)
    return params, pairing, g1, g, p


def setup_10():
    params = Parameters(n=3559 * 3571)
    pairing = Pairing(params)

    # g = Element.random(pairing, G2)
    # g1 = Element.random(pairing, G1)
    g = Element(pairing, G2, value=g2_10)
    g1 = Element(pairing, G1, value=g1_10)
    # g = Element(pairing, G2, value=g2s)
    # g1 = Element(pairing, G1, value=g1s)
    p = 457530803
    # print(params)
    return params, pairing, g1, g, p


def kg(pairing, g):
    # pairing = Pairing(params)
    sk = Element.random(pairing, Zr)
    # pk = Element(pairing, G1, value=g ** sk)
    pk = Element(pairing, G1, value=pow(g, sk))
    return (sk, pk)


def kg_mdvs(pairing, g):
    # pairing = Pairing(params)
    sk = Element.random(pairing, Zr)
    # pk = Element(pairing, G1, value=g ** sk)
    pk = Element(pairing, G2, value=pow(g, sk))
    return (sk, pk)


def binary_to_hex(binary_string):
    decimal_number = int(binary_string, 2)
    # decimal_number = int(binary_string)

    hex_string = hex(decimal_number)[2:]

    return hex_string


def hex_to_binary(hex_string):
    decimal_number = int(hex_string, 16)

    binary_string = bin(decimal_number)[2:]
    return binary_string


def xor_strings_bitwise(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Binary strings must have the same length.")

    result = ''.join(str(int(a) ^ int(b)) for a, b in zip(s1, s2))

    return result


def enc(pairing, g, pk, m):
    y = Element.random(pairing, Zr)
    c1 = pow(g, y)
    pky = pow(pk, y)
    # pkyi = int(pky.__str__(), 16)
    pkys = hash_enc(pky)
    c2 = xor_strings_bitwise(m, pkys[:len(m)])
    # c2 = m ^ pkyi
    # print(c2)
    # c2s = Element(pairing, G2, value=c2)
    return (c1, c2)


def dec(sk, c1, c2):
    # pairing = Pairing(params)
    c1sk = pow(c1, sk)
    # c1sk_inv = ~c1sk
    sks = hash_enc(c1sk)
    # return c2 * c1sk_inv
    # return int(c2.__str__(), 16) ^ int(c1sk_inv.__str__(), 16)
    return xor_strings_bitwise(c2, sks[:len(c2)])


def e(pairing, g1, g2):
    return pairing.apply(g1, g2)


def sign(pairing, g, p, m, pkr, sks, l):
    r = hashs(m)
    h = hash0(pairing, g, p, m, r)
    s = hash1(e(pairing, pkr, pow(h, sks)), l)
    return (r, s)


def verify(pairing, m, g, p, pks, skr, σ, l):
    r = σ[0]
    s = σ[1]
    h = hash0(pairing, g, p, m, r)
    h1 = hash1(e(pairing, pks, pow(h, skr)), l)
    if s == h1:
        return 1
    else:
        return 0


def sign_bls(pairing, g1, g2, p, m, sk, l):
    h = hash(pairing, g1, p, m)
    s = e(pairing, pow(h, sk), g2)
    σ = hash_bls(s, l)
    return σ, h


def verify_bls(pairing, h, pk, σ, l):
    # e1 = e(pairing, σ, g2)
    e1 = σ
    e2 = hash_bls(e(pairing, h, pk), l)
    if e1 == e2:
        return 1
    else:
        return 0


def sign_mdvs(pairing, m, sks, pks, pkv, g):
    Y = Element.one(pairing, G2)
    h = []
    for i in range(len(pkv)):
        h.append(Element(pairing, Zr, value=hash_mdvs([pks, pkv[i], m, i])))
        Y = Y * Element(pairing, G2, value=pow(pkv[i], h[i]))
    r, c2, z2 = Element.random(pairing, Zr), Element.random(pairing, Zr), Element.random(pairing, Zr)
    T1 = Element(pairing, G2, value=pow(g, r))
    T2 = Element(pairing, G2, value=pow(Y, c2) * pow(g, z2))
    datas = [T1, T2, pks]
    for i in range(len(pkv)):
        datas.append(pkv[i])
    datas.append([m, Y])
    c = Element(pairing, Zr, value=hash_mdvs(datas))
    c1 = c - c2
    z1 = r - c1 * sks
    return (c1, c2, z1, z2)


def verify_mdvs(pairing, m, pks, c1x, c2x, z1x, z2x, pkv, g):
    c1 = Element(pairing, Zr, value=c1x)
    c2 = Element(pairing, Zr, value=c2x)
    z1 = Element(pairing, Zr, value=z1x)
    z2 = Element(pairing, Zr, value=z2x)
    Y = Element.one(pairing, G2)
    h = []
    for i in range(len(pkv)):
        h.append(Element(pairing, Zr, value=hash_mdvs([pks, pkv[i], m, i])))
        Y = Y * Element(pairing, G2, value=pow(pkv[i], h[i]))
    T1 = pow(pks, c1) * pow(g, z1)
    T2 = pow(Y, c2) * pow(g, z2)
    datas = [T1, T2, pks]
    for i in range(len(pkv)):
        datas.append(pkv[i])
    datas.append([m, Y])
    c = Element(pairing, Zr, value=hash_mdvs(datas))
    if c == c1 + c2:
        return 1
    else:
        return 0


def test_mdvs(pairing, g1, g, p):
    users = kg_mdvs(pairing, g)
    print("users == ", users)
    userr1 = kg_mdvs(pairing, g)
    userr2 = kg_mdvs(pairing, g)
    σ = sign_mdvs(pairing, "hello", users[0], users[1], [userr1[1], userr2[1]], g)
    print(σ)
    xs1 = hex_to_binary(str(σ[0])).zfill(16)
    xs2 = hex_to_binary(str(σ[1])).zfill(16)
    xs3 = hex_to_binary(str(σ[2])).zfill(16)
    xs4 = hex_to_binary(str(σ[3])).zfill(16)
    #print(xs1,xs2,xs3,xs4)
    #c1 = binary_to_hex(xs1)
    #c2 = binary_to_hex(xs2)
    #z1 = binary_to_hex(xs3)
    #z2 = binary_to_hex(xs4)
    c1 = int(σ[0])
    c2 = int(σ[1])
    z1 = int(σ[2])
    z2 = int(σ[3])
    print(c1,c2,z1,z2,"int")
    c1 = int(xs1,2)
    c2 = int(xs2,2)
    z1 = int(xs3,2)
    z2 = int(xs4,2)
    print(c1,c2,z1,z2,"bin")
    # print(σ)
    # print(hash_mdvs_bin(σ[0]))
    # print(hash_mdvs(σ[0]), hash_mdvs(σ[1]), hash_mdvs(σ[2]), hash_mdvs(σ[3]))
    print(verify_mdvs(pairing, "hello", users[1], c1, c2, z1, z2, [userr1[1], userr2[1]], g))
    # x1 = bin(int(σ[0].__str__(), 16))[2:92]
    # x2 = bin(int(σ[1].__str__(), 16))[2:92]
    # x3 = bin(int(σ[2].__str__(), 16))[2:92]
    # x4 = bin(int(σ[3].__str__(), 16))[2:92]
    # x = x1 + x2 + x3 + x4
    # x = "{}{}{}{}".format(int(σ[0].__str__(), 16), int(σ[1].__str__(), 16), int(σ[2].__str__(), 16),
    #                       int(σ[3].__str__(), 16))
    # c = enc(pairing, g, users[1], x)
    # ms = dec(users[0], c[0], c[1])

    print(xs1, len(xs1))
    print(xs2, len(xs2))
    print(xs3, len(xs3))
    print(xs4, len(xs4))
    # print(ms == x)
    # print(ms)
    # print("=====================================================================")
    # print(x)


def test_bls(pairing, g1, g, p, l):
    users = kg(pairing, g)
    userr = kg(pairing, g)
    σ, h = sign_bls(pairing, g1, g, p, "hello", users[0], l)
    h2 = hash(pairing, g1, p, "hello")
    print(verify_bls(pairing, h2, users[1], σ, l))
    hs = hash1("hello", 9)
    print(hs)


def test_dvs(pairing, g1, g, p):
    users = kg(pairing, g)
    userr = kg(pairing, g)
    σ = sign(pairing, g, p, "hello", users[1], userr[0], 3)
    print(verify(pairing, "hello", g, p, users[1], userr[0], σ, 3))


def main():
    # params, pairing, g1, g, p = setup_128()
    # params, pairing, g1, g, p = setup_10()
    # params, pairing, g1, g, p = setup_32()
    params, pairing, g1, g, p = setup_16()
    test_mdvs(pairing, g1, g, p)
    # test_bls(pairing, g1, g, p)
    # test_dvs(pairing, g1, g, p)
    # users = kg(pairing, g)
    # userr = kg(pairing, g)
    # # σ = sign(pairing, g, p, "hello", users[1], userr[0],3)
    # σ, h = sign_bls(pairing, g1, g, p, "hello", users[0])
    # # print(verify(pairing, "hello", g, p, users[1], userr[0], σ,3))
    # h2 = hash(pairing, g1, p, "hello")
    # print(verify_bls(pairing, h2, users[1], σ))
    # hs = hash1("hello", 9)
    # print(hs)

    # print(x)
    # print(verify_mdvs(pairing, "hello", users[1], σ[0], σ[1], σ[2], σ[3], [userr1[1], userr2[1]], g))


if __name__ == "__main__":
    main()

