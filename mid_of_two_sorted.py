# def g(m, n, ii):
#     print(m, n, ii)
#     if len(m) <= 0 or len(n) <= 0:
#         return
#     imm = int((len(m) - 1) / 2)
#     imn = int((len(n) - 1) / 2)
#     mm = m[imm]
#     mn = n[imn]
#
#     if mm < mn:
#         if ii < imm:
#             g(m[:imm], n[:imn], ii)
#         elif ii > len(m) + imn:
#             g(m[imm:], n[imn:], ii)


# def midx(m, n, i):
#     return m[i] if i < len(m) else n[i - len(m)]


def f(m, n, mb, me):
    ii = int((len(m) + len(n)) / 2)  # end
    if me - mb <= 1:
        nb = ii - mb - 1
        if (len(m) + len(n)) % 2 == 1:
            return max(m[mb], n[nb])
        else:
            return (m[mb] + n[nb]) / 2

    mi = int((mb + me) / 2)
    ni = ii - mi - 1
    km = m[mi]  # if mi < len(m) else n[mi - len(m)]
    kn = n[ni]

    print(km, kn)
    if km <= kn:
        return f(m, n, mi, me)
    else:
        return f(m, n, mb, mi)


def f1(m, n):
    if not n:
        return m[int(len(m) / 2)]
    return f(m, n, 0, len(gm))


gm = [10000]
gn = [10001]
l = list(sorted(gm + gn))
print(l)
print(':::', f1(gm, gn))
