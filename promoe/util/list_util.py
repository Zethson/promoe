def group(seq, sep):
    grp = []
    for el in seq:
        if el == sep:
            yield grp
            grp = []
        grp.append(el)
    yield grp
