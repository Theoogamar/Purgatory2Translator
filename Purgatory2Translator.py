from googletrans import Translator
import os, pickle

# make dirs for things
os.makedirs("MapData", exist_ok=True)
os.makedirs("pickles", exist_ok=True)
os.makedirs("pickles/MapData", exist_ok=True)
os.makedirs("pickles/Choices", exist_ok=True)

# main varables
translator = Translator(service_urls=["translate.google.com.au"]) # , "translate.google.com"
Source = r"Data/MapData"
maps = os.listdir(Source)

count = 0
for file in maps:

    # do 30 translations everyday to stop getting ip banned lmao
    if (count >= 30):
        quit()

    print (file)

    # Read the map file as binary
    filename = os.path.join(Source, file)
    DATA = open(filename, "rb").read()
    data = bytearray()

    japanese = []
    replace = False
    start = 0

    # scrapes the japanese text
    for i in range(len(DATA)):

        # check for the "@" symbol
        if (not replace):
            if (DATA[i] == 64):
    
                # then check for the "\n" symbol
                if (DATA[i + 2] == 10):
                    replace = True
                    start = i + 3
    
                elif (DATA[i + 3] == 10):
                    replace = True
                    start = i + 4
    
                elif (DATA[i + 4] == 10 and DATA[i + 2] != 0):
                    replace = True
                    start = i + 5
    
                elif (DATA[i + 5] == 10):
                    raise Exception(f"there's something at: {file}, {DATA[i:i+20].decode('shift-jis')}")

        if (replace):
            if (DATA[i] == 0 or DATA[i] == 1):
                text = DATA[start:i].decode("shift-jis").replace("\n", "")
                japanese.append(text)
                replace = False

    count += 1

    if (True):

        # translate the text
        print ("translating...")
        english = [translator.translate(jap, src="ja", dest="en").text for jap in japanese]
        print (english)

        with open(os.path.join("pickles/MapData", file.replace("mps", "pickle")), 'wb') as handle:
            pickle.dump(english, handle)

    else:

        # load translated text
        with open(f'pickles/MapData/{pickles[i]}', 'rb') as handle:
            english = pickle.load(handle)

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

            # add a new line every 40 charicters
            if ((i + 1) % 40 == 0):
                newline = True
            if (newline and english[idx][i] == " "):
                str += "\n"
                newline = False

        # replace illegal charaicters
        str = str.replace("\u200b", "")
        str = str.replace("\xab", "<")
        str = str.replace("\xbb", ">")

        # fix Enri's miss translations
        #str = str.replace("(Kokun)", "*nods*")
        #str = str.replace("(Ko-kun)", "*nods*")
        #str = str.replace("Furu Furu", "*shivering*"

        return str.encode("shift-jis")

    # prepares the string return data that helps add the english text
    def editData(idx, j):

        text = fixSpecialCharaicters(idx)

        # checks if the lenght is bigger than a byte
        assert len(text) + j < 255, "hmmm"

        # adds the lenght of the string in the file because reasons
        data[len(data) - 5:len(data) - 4] = bytes([len(text) + j])

        # add the charicters it skips over
        for j in range(1, (j - 1)):
            data.append(DATA[i + j])

        return True, len(data) + (j - 1), text

    idx = 0
    replace = False

    # goes through and adds in the english text
    for i in range(len(DATA)):

        if (not replace):
            data.append(DATA[i])

            if (DATA[i] == 64):

                if (DATA[i + 2] == 10):
                    replace, start, text = editData(idx, 4)

                elif (DATA[i + 3] == 10):
                    replace, start, text = editData(idx, 5)

                elif (DATA[i + 4] == 10 and DATA[i + 2] != 0):
                    replace, start, text = editData(idx, 6)

        else:
            if (DATA[i] == 0 or DATA[i] == 1):

                # adds the new text
                data[start:i] = text

                # add the charater it misses
                data.append(DATA[i])

                idx += 1
                replace = False

    # write new map file
    with open(os.path.join("MapData", file), "wb") as f:
        f.write(data)
        f.close()

    print ()
