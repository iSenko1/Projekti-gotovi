import numpy as np

vowels = "aáeéiíoóuúü"
vowels += vowels.upper()
vowels = set(i for i in vowels)
constants = "bcdfghjklmnñpqrstvwxyz"
constants += constants.upper()
constants = set(i for i in constants)
# print(vowels)
# print(constants)

VOWELS11 = "aáeéiíoóuúü"
VOWELS11 += VOWELS11.upper()
CONSONANTS11 = "bcdfghjklmnñpqrstvwxyz"
CONSONANTS11 += CONSONANTS11.upper()
bilabijalni = ["pr", "br", "pl", "bl", "fr", "fl"]
velarni = ["gr", "gl", "cr", "cl"]
zubni = ["dr", "tr", "Dr", "Tr"]
NIZ32 = ["ns", "bs", "Ns", "Bs"]
JAKI = list("aeoáéóAEOÁÉÓ")
SLABI = list("iíuúüIÍUÚÜ")
AKCENT_SLABI = list("íúüaeoáéóÍÚÜAEOÁÉÓ")
VOWELS11 = set(i for i in VOWELS11)
CONSONANTS11 = set(i for i in CONSONANTS11)

# JAKI_PERM = []
# for p in JAKI:
#     for d in JAKI:
#         JAKI_PERM.append(p + d)

BILABIJALNI = []
for i in bilabijalni:
    BILABIJALNI.append(i.capitalize())
bilabijalni += BILABIJALNI

VELARNI = []
for i in bilabijalni:
    VELARNI.append(i.capitalize())
velarni += VELARNI


# print(JAKI_PERM)


# Napraviti da korisnik bira ako hoće samo riječ ili csv i ovisno šta hoće
# pokaže mu se polje za unos ili link za odabir datoteke


def pretvorba_2(ulazStr):
    izlazStr = []
    counter = 0

    # if len(ulazStr) == 2 and ulazStr[0] in JAKI and ulazStr[1] in JAKI:
    #     izlazStr.append(''.join(ulazStr[0]))
    #     izlazStr.append(''.join(ulazStr[1]))
    #     return izlazStr
    """
    --------------------------------PRAVILA 4 / 8-----------------------------------------------
    """
    i = 0
    while i < len(ulazStr):
        # print('pretvorb3 4 / 8')
        if i + 1 >= len(ulazStr):
            break
        if (
            ulazStr[i] in JAKI
            and ulazStr[i + 1] in JAKI
            or ulazStr[i] in AKCENT_SLABI
            and ulazStr[i + 1] in AKCENT_SLABI
        ):
            izlazStr.append("".join(ulazStr[: i + 1].split()))
            izlazStr.append("".join(ulazStr[i + 1 :].split()))
            break
        i += 1

    if izlazStr:
        return izlazStr

    """
    --------------------------------PRAVILO 3-----------------------------------------------
    """
    if len(ulazStr) > 4:
        i = 0
        # print('pretvorba 3.1 / 3.2')
        while i < len(ulazStr):
            if ulazStr[i] in VOWELS11:
                counter = i + 1
                prolaz = 0
                while ulazStr[counter] in CONSONANTS11:
                    prolaz += 1
                    counter += 1
                    if counter >= len(ulazStr):
                        break
                if ulazStr[counter] in VOWELS11 and prolaz > 2:
                    if ulazStr[i + 1 : i + 3] in NIZ32:
                        izlazStr.append("".join(ulazStr[: i + 3].split()))
                        izlazStr.append("".join(ulazStr[i + 3 :].split()))
                    else:
                        izlazStr.append("".join(ulazStr[: counter - 2].split()))
                        izlazStr.append("".join(ulazStr[counter - 2 :].split()))
                    i = counter + 1
                    #
                    break
                else:
                    break
            i += 1
            if counter >= len(ulazStr) or i >= len(ulazStr):
                break
        if izlazStr:
            return izlazStr

    """
    --------------------------------PRAVILO 2-----------------------------------------------
    """
    i = 0
    while i < len(ulazStr):
        # pretvorba 2.1
        if (
            ulazStr[i] in VOWELS11
            and ulazStr[i + 1 : i + 3] in bilabijalni
            and ulazStr[i + 3] in VOWELS11
        ):
            izlazStr.append("".join(ulazStr[: i + 1].split()))
            izlazStr.append("".join(ulazStr[i + 1 :].split()))
            if ulazStr[i + 3 :] == "":
                break
        i += 1
    if izlazStr:
        return izlazStr
    # ------------------------------------------------------------------------------------
    i = 0
    while i < len(ulazStr):
        # print('pretvorba 2.2')
        if (
            ulazStr[i] in VOWELS11
            and ulazStr[i + 1 : i + 3] in velarni
            and ulazStr[i + 3] in VOWELS11
        ):
            izlazStr.append("".join(ulazStr[: i + 1].split()))
            izlazStr.append("".join(ulazStr[i + 1 :].split()))
            if ulazStr[i + 3 :] == "":
                break
        i += 1
    if izlazStr:
        return izlazStr
    # ------------------------------------------------------------------------------------
    i = 0
    while i < len(ulazStr):
        # print('pretvorba 2.3')
        if (
            ulazStr[i] in VOWELS11
            and ulazStr[i + 1 : i + 3] in zubni
            and ulazStr[i + 3] in VOWELS11
        ):
            izlazStr.append("".join(ulazStr[: i + 1].split()))
            izlazStr.append("".join(ulazStr[i + 1 :].split()))
            if ulazStr[i + 3 :] == "":
                break
        i += 1
    if izlazStr:
        return izlazStr
    # ------------------------------------------------------------------------------------
    i = 0
    while i < len(ulazStr):
        # print('pretvorba 2.4')
        if i + 3 >= len(ulazStr):
            break
        if (
            ulazStr[i] in VOWELS11
            and ulazStr[i + 1 : i + 3] == "tl"
            and ulazStr[i + 3] in VOWELS11
        ):
            izlazStr.append("".join(ulazStr[: i + 1].split()))
            izlazStr.append("".join(ulazStr[i + 1 :].split()))
            if ulazStr[i + 3 :] == "":
                break
        i += 1
    if izlazStr:
        return izlazStr
    i = 0
    # ------------------------------------------------------------------------------------
    while i < len(ulazStr):
        # pretvorba 2.5
        if i + 3 >= len(ulazStr):
            break
        # if i + 3 >= len(ulazStr) and not izlazStr:
        #     return ulazStr
        if (
            ulazStr[i] in VOWELS11
            and ulazStr[i + 1] in CONSONANTS11
            and ulazStr[i + 2] in CONSONANTS11
            and ulazStr[i + 3] in VOWELS11
        ):
            izlazStr.append("".join(ulazStr[: i + 2].split()))
            izlazStr.append("".join(ulazStr[i + 2 :].split()))
            i += 4
            continue

        if i + 3 >= len(ulazStr):
            break
        i += 1
    if izlazStr:
        return izlazStr

    """
    --------------------------------PRAVILO 1-----------------------------------------------
    """
    #   ISPOD JE PRETVORBA 1
    i = 0
    while True:
        if i + 2 >= len(ulazStr):
            break
        if (
            ulazStr[i] in VOWELS11
            and ulazStr[i + 1] in CONSONANTS11
            and ulazStr[i + 2] in VOWELS11
        ):
            izlazStr.append("".join(ulazStr[: i + 1].split()))
            izlazStr.append("".join(ulazStr[i + 1 :].split()))
            i += 3
            break
        if i + 2 >= len(ulazStr):
            break
        i += 1
    if izlazStr:
        return izlazStr

    if not izlazStr:
        izlazStr = izlazStr.append(ulazStr)
        return izlazStr


def pretvorbe_sve(rijecTest):
    output = []

    if "ü" in rijecTest:
        output.append(rijecTest)
        return output

    n = 0
    if pretvorba_2(rijecTest):
        output = pretvorba_2(rijecTest)
        while n < len(output):
            if len(output[n]) > 1:
                zadnje = pretvorba_2(output[n])
                if zadnje:
                    output.pop(n)
                    for i in zadnje[::-1]:
                        output.insert(n, i)
            n += 1
            if any(pretvorba_2(x) for x in output) and n == len(output):
                n = 0

        return output
    else:
        #   ako nema nista u listi onda samo vrati pocetni rijeci
        output.append(rijecTest)
        return output


# ----------------------------DRUGI DIO ZADATKA---------------------------------------------
listaProvjera = []
listaTocno = []
with open("Spanjolski-Slogovi-python/tekstProvjera.txt", encoding="utf-8") as f:
    contents = f.read()
    contents = contents.split()
    contents = [i for i in contents if len(i) > 1]
    i = 0
    while i < len(contents):
        if i % 2 == 0:
            # print(contents[i].replace('"', ''))
            listaProvjera.append(contents[i].replace('"', ""))
        if i % 2 != 0:
            listaTocno.append((contents[i].replace('"', "")).split("."))
        i += 1

izlazLista = ""
izlazLista2 = ""
n = 0
count = 0
izlazLista00 = []
izlazLista11 = []
oznake = "Pogrešno je:\n\n"
kriveRijeci = []
tocneRijeci = []

for rijeci in listaProvjera:
    izlazLista00.append(".".join(pretvorbe_sve(rijeci)))
    izlazLista11.append(".".join(listaTocno[n]))
    izlazLista += ".".join(pretvorbe_sve(rijeci)) + " "
    izlazLista2 += ".".join(listaTocno[n]) + " "

    if pretvorbe_sve(rijeci) != listaTocno[n]:
        # print('Netocno', pretvorbe_sve(rijeci))
        kriveRijeci.append(pretvorbe_sve(rijeci))
        tocneRijeci.append(listaTocno[n])
        oznake += ".".join(pretvorbe_sve(rijeci)) + "\n"
        # print('Tocno', listaTocno[n])
        count += 1
    n += 1

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score

zipLista = list(zip(listaProvjera, izlazLista00, izlazLista11))

df = pd.DataFrame(zipLista, columns=["Pocetno", "Moje", "Tocno"])
df["PROVJERA"] = np.where((df["Moje"] != df["Tocno"]), False, True)
df["Brojevi"] = np.where((df["PROVJERA"] == True), 1, 1)

novaLista = []
counter = 0
for r in range(len(kriveRijeci)):
    for rr in range(len(kriveRijeci[r])):
        if kriveRijeci[r][rr] != tocneRijeci[r][rr]:
            counter += 1
    novaLista.append([".".join(kriveRijeci[r]), counter])
    counter = 0
print(f"nova lista je: {novaLista}")
print("\n")

true_values = df["PROVJERA"].value_counts()[True]
false_values = df["PROVJERA"].value_counts()[False]
labels = ["Točno", oznake]
values = [true_values, false_values]

rezDict = {}
for i in novaLista:
    rezDict[i[0]] = i[1]

kljkucevi = list(rezDict.keys())
values1 = list(rezDict.values())

# Prvi način
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle("Izvješče o točnosti")

# -------------------------------------
# PIE PLOT
ax1.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    explode=[0.05, 0.1],
    shadow=True,
    startangle=45,
)
ax1.legend(values, loc="upper left")
ax1.axis("equal")

# BAR PLOT
ax2.bar(kljkucevi, values1, width=0.3, edgecolor="#820000")
for i, v in enumerate(values1):
    ax2.text(i - 0.03, v + 0.1, str(v), color="#820000", fontweight="bold")
ax2.set(xlabel="Broj pogrešnih slogova", ylabel="Pogrešne riječi")

# FORMULA ZA ISPISIVANJE TOČNOSTI MODELA
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

mojeVr = df["Moje"]
tocneVr = df["Tocno"]
tocnost = accuracy_score(mojeVr, tocneVr)
print((tocnost * 100).__round__(2))
print(precision_recall_fscore_support(mojeVr, tocneVr, average="micro"))
plt.show()
