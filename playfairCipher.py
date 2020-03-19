def playfairEcrypt(text):
    text = text.replace(" ", "")
    text = text.upper()
    listPair = []
    c = 0
    while c < len(text):
        if c + 1 < len(text):
            if text[c] == text[c + 1]:
                listPair.append((text[c], 'x'))
                c += 1
                continue
            listPair.append((text[c], text[c + 1]))
            c += 2
            continue
        listPair.append((text[c], 'x'))
        c += 1


    key = [["P", "L", "A", "Y", "F"],
           ["I", "R", "E", "X", "M"],
           ["B", "C", "D", "G", "H"],
           ["K", "N", "O", "Q", "S"],
           ["T", "U", "V", "W", "Z"]]
    listEncrPair = []
    ccheck1 = False
    ccheck2 = False
    while len(listPair) > 0:
        pair = listPair[0]
        pos1 = -1
        pos2 = -1
        for row in key:
            if (pair[0] in row) & (pair[1] in row):
                for item in row:
                    if pair[0] == item:
                        pos1 = row.index(item)+1
                        if pos1 > 4:
                            pos1 -= 5
                    if pair[1] == item:
                        pos2 = row.index(item)+1
                        if pos2 > 4:
                            pos2 -= 5
                listEncrPair.append((row[pos1], row[pos2]))
                listPair.pop(0)


            # WORK ON "COLUMN CASE"
            if pair[0] == row[0]:
                ccheck1 = True
                pos1 = key.index(row) + 1
                if pos1 > 4:
                    pos1 -= 5
            if pair[1] == row[0]:
                ccheck2 = True
                pos2 = key.index(row) + 1
                if pos2 > 4:
                    pos2 -= 5

            if ccheck1 & ccheck2:
                listEncrPair.append((key[pos1], key[pos2]))

            # ADD CHECK FOR "RECTANGLE CASE"

    print(listEncrPair)
    print(listPair)

playfairEcrypt("pt yl  fa bg")
