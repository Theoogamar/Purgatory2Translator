from googletrans import Translator
import os, pickle

# main varables
translator = Translator(service_urls=["translate.google.com.au"])
Source = r"Data/BasicData/DataBase.dat"

DATA = open(Source, "rb").read()
data = bytearray()

japanese = []
state = 0
start = 0

# scrapes the japanese text
for i in range(len(DATA)):

    if (state == 0):

        # check for ] and a number bettween 0-9
        if (DATA[i] == 93 and 48 <= DATA[i - 1] <= 57):

            start = i + 1
            state = 1          

    elif (state == 1):

        # check for null or \ (backslash)
         if (DATA[i] == 0 or DATA[i] == 92):

             japanese.append(DATA[start:i].decode("shift-jis"))
             e = DATA[start:i].decode("shift-jis")

             state = 2

    elif (state == 2):

        # check for japanese text or \ (backslash) or letter between A-Z
        if (DATA[i] > 127 or DATA[i] == 92 or 65 <= DATA[i] <= 90):

            start = i
            state = 3

    elif (state == 3):

        # check for null or between A-Z
        if (DATA[i] == 0):

            japanese.append(DATA[start:i].decode("shift-jis"))
            state = 0

if (True):

    # translate the text
    print ("translating...")
    english = [translator.translate(jap, src="ja", dest="en").text for jap in japanese]
    print (english)

    # save the translated text
    with open(os.path.join("pickles", "DataBase.pickle"), 'wb') as handle:
        pickle.dump(english, handle)

else:

    # load the translated text
    with open(os.path.join("pickles", "DataBase.pickle"), 'rb') as handle:
        english = pickle.load(handle)
        #print (english)

# function for fixing special charaicters
def fixSpecialCharaicters(idx):

    # remove spaces in special charaicters e.g. \ f [9] to \f[9]
    replace = True
    newline = False
    str = ""
    for i in range(len(english[idx])):
        if (replace):
            str += english[idx][i]

            if (english[idx][i] == "\\"):
                replace = False
        else:
            if (english[idx][i] != " "):
                str += english[idx][i]
            if (english[idx][i - 1] == "]"):
                replace = True

    return str.encode("shift-jis")

state = 0
idx = 0

# goes through and adds in the english text
for i in range(len(DATA)):

    if (state == 0):

        data.append(DATA[i])

        # check for ] and a number bettween 0-9
        if (DATA[i] == 93 and 48 <= DATA[i - 1] <= 57):

            state = 1          

    elif (state == 1):

        # check for null or \ (backslash)
        if (DATA[i] == 0 or DATA[i] == 92):

            # adds the new text
            start = len(data)
            data[start:i] = fixSpecialCharaicters(idx)

            # gets the index to place the lenght of string
            for j in range(start, 10, -1):
                 if (data[j] == 92):
                     j = start - j
                     break

            # adds the lenght of the string in the file because of some bullshit to do with encoding or something idk
            data[start - j - 4] = len(fixSpecialCharaicters(idx)) + j + 1
            idx += 1

            state = 2

            data.append(DATA[i])

    elif (state == 2):

        # check for japanese text or \ (backslash) or letters between A-Z
        if (DATA[i] > 127 or DATA[i] == 92 or 65 <= DATA[i] <= 90):

            state = 3
            continue

        data.append(DATA[i])

    elif (state == 3):

        # check for null
        if (DATA[i] == 0):

            # adds the new text
            start = len(data)
            data[start:i] = fixSpecialCharaicters(idx)

            # adds the lenght of the string in the file because of some bullshit to do with encoding or something idk
            data[start - 4] = len(fixSpecialCharaicters(idx)) + 1
            idx += 1

            state = 0

            data.append(DATA[i])

# write new data file
with open("DataBase.dat", "wb") as f:
    f.write(data)
    f.close()
