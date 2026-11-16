"""Encodeur QR minimal : version 3, niveau L, mode octet, masque 0."""
import sys

# --- GF(256) ---
EXP = [0] * 512
LOG = [0] * 256
x = 1
for i in range(255):
    EXP[i] = x
    LOG[x] = i
    x <<= 1
    if x & 0x100:
        x ^= 0x11D
for i in range(255, 512):
    EXP[i] = EXP[i - 255]


def gmul(a, b):
    return 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]


def rs_ec(data, n):
    gen = [1]
    for i in range(n):
        gen = [a ^ b for a, b in zip(gen + [0], [0] + [gmul(c, EXP[i]) for c in gen])]
    # gen est en ordre croissant de degre inverse : recalcul en ordre descendant
    gen = [1]
    for i in range(n):
        new = [0] * (len(gen) + 1)
        for j, c in enumerate(gen):
            new[j] ^= c
            new[j + 1] ^= gmul(c, EXP[i])
        gen = new
    rem = list(data) + [0] * n
    for i in range(len(data)):
        coef = rem[i]
        if coef:
            for j in range(1, len(gen)):
                rem[i + j] ^= gmul(gen[j], coef)
    return rem[len(data):]


def format_bits(ec_bits, mask):
    d = (ec_bits << 3) | mask
    v = d << 10
    g = 0b10100110111
    for i in range(14, 9, -1):
        if v & (1 << i):
            v ^= g << (i - 10)
    return ((d << 10) | v) ^ 0b101010000010010


def encode(text, version=3, data_cw=55, ec_cw=15):
    size = 17 + 4 * version
    raw = text.encode("utf-8")
    bits = "0100" + format(len(raw), "08b") + "".join(format(b, "08b") for b in raw)
    cap = data_cw * 8
    bits += "0" * min(4, cap - len(bits))
    bits += "0" * (-len(bits) % 8)
    cws = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    pad = [0xEC, 0x11]
    i = 0
    while len(cws) < data_cw:
        cws.append(pad[i % 2])
        i += 1
    allcw = cws + rs_ec(cws, ec_cw)
    stream = "".join(format(c, "08b") for c in allcw)

    M = [[None] * size for _ in range(size)]

    def finder(r, c):
        for dr in range(-1, 8):
            for dc in range(-1, 8):
                rr, cc = r + dr, c + dc
                if 0 <= rr < size and 0 <= cc < size:
                    inside = 0 <= dr <= 6 and 0 <= dc <= 6
                    on = inside and (dr in (0, 6) or dc in (0, 6) or (2 <= dr <= 4 and 2 <= dc <= 4))
                    M[rr][cc] = 1 if on else 0

    finder(0, 0)
    finder(0, size - 7)
    finder(size - 7, 0)
    for k in range(8, size - 8):
        M[6][k] = M[k][6] = 1 if k % 2 == 0 else 0
    # alignement (version 3 : centre 22,22)
    ac = 4 * version + 10
    for dr in range(-2, 3):
        for dc in range(-2, 3):
            M[ac + dr][ac + dc] = 1 if max(abs(dr), abs(dc)) != 1 else 0
    M[size - 8][8] = 1  # module sombre
    # zones de format reservees
    reserved = set()
    for k in range(9):
        reserved.add((8, k)); reserved.add((k, 8))
    for k in range(8):
        reserved.add((8, size - 1 - k)); reserved.add((size - 1 - k, 8))
    for r, c in reserved:
        if M[r][c] is None:
            M[r][c] = 0
    func = [[M[r][c] is not None for c in range(size)] for r in range(size)]
    for r, c in reserved:
        func[r][c] = True

    # placement en zigzag
    idx = 0
    col = size - 1
    upward = True
    while col > 0:
        if col == 6:
            col -= 1
        rows = range(size - 1, -1, -1) if upward else range(size)
        for r in rows:
            for c in (col, col - 1):
                if not func[r][c]:
                    b = int(stream[idx]) if idx < len(stream) else 0
                    idx += 1
                    if (r + c) % 2 == 0:  # masque 0
                        b ^= 1
                    M[r][c] = b
        upward = not upward
        col -= 2

    fb = format_bits(0b01, 0)  # niveau L = 01
    fbits = [(fb >> (14 - i)) & 1 for i in range(15)]
    pos1 = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8), (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]
    pos2 = [(size - 1, 8), (size - 2, 8), (size - 3, 8), (size - 4, 8), (size - 5, 8), (size - 6, 8), (size - 7, 8),
            (8, size - 8), (8, size - 7), (8, size - 6), (8, size - 5), (8, size - 4), (8, size - 3), (8, size - 2), (8, size - 1)]
    for b, (r, c) in zip(fbits, pos1):
        M[r][c] = b
    for b, (r, c) in zip(fbits, pos2):
        M[r][c] = b
    assert idx >= len(stream)
    return M


if __name__ == "__main__":
    # tests de reference (norme / thonky.com)
    ref = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    assert rs_ec(ref, 10) == [196, 35, 39, 119, 235, 215, 231, 226, 93, 23], rs_ec(ref, 10)
    assert format(format_bits(0b01, 0), "015b") == "111011111000100"
    assert format(format_bits(0b00, 0), "015b") == "101010000010010"
    print("tests ok")
    M = encode(sys.argv[1])
    print("\n".join("".join("#" if v else "." for v in row) for row in M))
