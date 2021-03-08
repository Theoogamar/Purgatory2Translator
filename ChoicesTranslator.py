from googletrans import Translator
import os, pickle

# main varables
translator = Translator(service_urls=["translate.google.com.au"])
Source = r"MapData"
maps = os.listdir(Source)

#idx = maps.index("Map145.mps") # 162, 145
#maps = maps[idx:]

for file in maps:

    # Read the map file as binary
    filename = os.path.join(Source, file)
    DATA = open(filename, "rb").read()
    data = bytearray()

    japanese = []
    replace = False
    find = False
    start = 0

    # scrapes the japanese text
    for i in range(len(DATA)):

        if (not replace):
            # check for the "f" symbols
            if (DATA[i] == 102):

                # check if out of bounds
                if (i < len(DATA) - 3):

                    # check for a 0, and 2 and 3 "null" symbols
                    if (DATA[i - 2] == 0 and DATA[i - 1] == 2 and DATA[i + 1] == 0 and DATA[i + 2] == 0 and DATA[i + 3] == 0):
                        replace = True

        # get the japanesse text
        if (replace):

            # check for the end
            if (DATA[i] == 145 and DATA[i - 1] == 2):
                replace = False
                continue

            # find the areas where the text lyes
            if (not find):
                if (DATA[i] > 127):
                    find = True
                    start = i

            # save the text
            if (find):
                if (DATA[i] == 0):
                    text = DATA[start:i].decode("shift-jis")
                    japanese.append(text)
                    find = False

    if (len(japanese) == 0):
        continue

    print (file)

    if (False):

        # translate the text
        print ("translating...")
        english = [translator.translate(jap, src="ja", dest="en").text for jap in japanese]
        print (english)

        # save the translated text
        with open(os.path.join("pickles/Choices", file.replace("mps", "pickle")), 'wb') as handle:
            pickle.dump(english, handle)
    else:

        with open(os.path.join("pickles/Choices", file.replace("mps", "pickle")), 'rb') as handle:
            english = pickle.load(handle)
            print (english)

    replace = False
    find = False
    idx = 0
    space = 0

    # goes through and adds in the english text
    for i in range(len(DATA)):

        if (not replace):

            data.append(DATA[i])

            # check for the "f" symbols
            if (DATA[i] == 102):

                # check if out of bounds
                if (i < len(DATA) - 3):

                    # check for a 0, and 2 and 3 "null" symbols
                    if (DATA[i - 2] == 0 and DATA[i - 1] == 2 and DATA[i + 1] == 0 and DATA[i + 2] == 0 and DATA[i + 3] == 0):
                        replace = True
                        continue

        if (replace):

            # check for the end
            if (DATA[i] == 145 and DATA[i - 1] == 2):
                data.append(DATA[i])
                replace = False
                continue

            # find the areas where the text lyes
            if (not find):

                if (DATA[i] > 127):

                    # adds the new text
                    start = len(data)
                    data[start:i] = english[idx].encode("shift-jis")

                    # adds the lenght of the string in the file because reasons
                    data[start - 4] = len(english[idx].encode("shift-jis")) + 1
                    idx += 1

                    find = True
                    continue

                data.append(DATA[i])

            # iterate to string end
            if (find):

                if (DATA[i] == 0):    
                    
                    data.append(DATA[i])
                    find = False
    
    # write new map file
    with open(os.path.join("MapData", file), "wb") as f:
        f.write(data)
        f.close()
