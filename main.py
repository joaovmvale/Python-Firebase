import requests
import json

from requests.api import delete

base_url = '[YOUR DABASE URL HERE]'

def getCurrentPhraseNumber(url):
    return requests.get(url + 'frase.json').json()

def getCurrentPhrase(url):
    number = requests.get(url + 'frase.json').json()
    phrase = requests.get(url + str(getCurrentPhraseNumber(url)) + '.json').json()
    print(f'{number}: {phrase}')

def getLastPhraseNumber(url):
    phraseNumber = getCurrentPhraseNumber(url)
    phraseText = requests.get(url + str(phraseNumber) + '.json').json()

    while phraseText != None:
        phraseNumber += 1
        phraseText = requests.get(url + str(phraseNumber) + '.json').json()

        if phraseText == None:
            return phraseNumber

def patchPhrase(url, phraseNumber):
    print(f"\n{getCurrentPhraseNumber(url)}: current number\n{getLastPhraseNumber(url)}: new number")
    phrase = input("\nObs: Use these + signals as reference of the maximum characters\nWrite your phrase below\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n:  ")
    if len(phrase) > 119:
        print("You can only write 119 characters.")
        menuView()
    else:
        data = {phraseNumber(url) : "  " + phrase}
        requests.patch(url + '.json', data=json.dumps(data))

def readPhrase(url):
    print("Please, write the number of the phrase you wanna read")
    phraseNumber = input(":  ")
    print(requests.get(url + phraseNumber + '.json').json())

def deletePhrase(url):
    try:
        print("Please, write the number of the phrase you wanna delete")
        phraseNumber = input(":  ")
        if phraseNumber.isdigit():
            phraseText = requests.get(url + phraseNumber + '.json').json()
            
            if phraseText != None:
                print(f"{phraseNumber}: {phraseText}")
                print("Sure to dele this phrase? (Y/N)")
                ans = input(":  ")
                res = ans.upper()
                if res in ['Y','N']:
                    requests.delete(url + phraseNumber + '.json')
                else:
                    print("\n**Make sure that your response is [Y] for yes or [N] for no! =D**\n")
                    deletePhrase(url)
            else:
                print("\n**That looks we don't have a phrase with this number :S, try again.**\n")
                deletePhrase(url)
        else:
            print("\n**Please, only numbers!**\n")
            deletePhrase(url)

    except ValueError:
        print("\n**Please, only letters. Use [Y] for yes and [N] for no. =D**\n")
        deletePhrase(url)

def menuController():
    try:
        option = int(input(":  "))

        if option in [1,2,3,4]:
            if option == 1:
                patchPhrase(base_url, getLastPhraseNumber)
            elif option == 2:
                readPhrase(base_url)
            elif option == 3:
                getCurrentPhrase(base_url)
            elif option == 4:
                deletePhrase(base_url)
            
        else:
            print("\nInvalid option, please try again.")
            menuView()

    except ValueError:
        print("\nPlease, only numbers :D")
        menuView()

def menuView():
    print("++++++++++++++++++++++++++++++++++++++")
    print("++               MENU               ++")
    print("++++++++++++++++++++++++++++++++++++++")
    print("++  1 - Input a phrase              ++")
    print("++  2 - Read a phrase               ++")
    print("++  3 - Read current phrase         ++")
    print("++  4 - Delete a phrase             ++")
    print("++  5 - Read last phrases           ++")
    print("+++++++++++++++++++++++++++++++++++ ++")

    menuController()

if __name__ == "__main__":
    menuView()