import requests
import json

base_url = 'https://bea-display-default-rtdb.firebaseio.com/'

def getCurrentPhraseNumber(url):
    return requests.get(url + 'frase.json').json()

def getLastPhraseNumber(url):
    phraseNumber = getCurrentPhraseNumber(url)
    phraseText = requests.get(url + str(phraseNumber) + '.json').json()

    while phraseText != None:
        phraseNumber += 1
        phraseText = requests.get(url + str(phraseNumber) + '.json').json()

        if phraseText == None:
            return phraseNumber

def patchMessage():
    patchData(base_url, getLastPhraseNumber)

def patchData(url, phraseNumber):
    phrase = input('Write your phrase: ')
    data = {phraseNumber(url) : "  " + phrase}
    requests.patch(url + '.json', data=json.dumps(data))

if __name__ == "__main__":
    patchMessage()