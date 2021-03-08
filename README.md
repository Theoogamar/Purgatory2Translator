
# WOLF RPG maker translator

 Translates games from WOLF RPG maker engine
 
 **ONLY tested for purgatory 2**
 
 For all that is unholy don't use the unofficial Google Translator API that i have used
 use the official Google translator on Google Cloud.
 
 The only bit i haven't translated is when you inspect an item
 don't know which file it is in, have to go looking
 todo: translate the last little bit
 
 Sorry for the messy code
 
 ## Getting Started
 
 **Python 3.7+**
 
 **pip install**
 * googletrans (unofficial Google Translator API)
 
 **How to use**
 * Use the [WOLF rpg extractor ](https://github.com/Sinflower/WolfDec) to extract the .wolf file
 * Put the extracted folder in root folder
 * Run Purgatory2Translator.py then ChoicesTranslator.py then ItemTranslator.py
 
 **How to play game**
 * Replace the translated mapdata (./MapData) with the untranslated mapdata (./Data/MapData)
 * Replace the translated items (./DataBase.dat) with the untranslated items (./Data/BasicData/DataBase.dat)
 * Download the [WOLF RPG Editor ](https://widderune.wixsite.com/widderune/wolf-rpg-editor-english) get the Full Package
 * In the WOLF RPG Editor directory copy "Config.exe", "Game.exe", "Game.ini", "GuruGuruSMF4.dll" into a new directory
 * Also copy the translated DATA folder and add that to the new directory
 * Run and enjoy google translated translations

## Purgatory2Translator.py

Translates the dialog
	
TODO: add more

## ChoicesTranslator.py

Translates the choices
	
**run Purgatory2Translator.py before running ChoicesTranslator.py**
	
TODO: add more

## ItemTranslator.py

Translates the items
	
TODO: add more
