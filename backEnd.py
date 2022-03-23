import json
from difflib import get_close_matches

data = json.load(open("data.jdbx"))
Keys = list(data.keys())
Keys.sort()

def exe(word):
    finalRes= [out for out in data[word]]
    return finalRes

def main(word1):
    try:
        if word1 in data:
            return exe(word1)
        else:
            word2 = word1.lower()
            if word2 in data:
                return exe(word2)
            else:
                word3 = get_close_matches(word1, Keys, 20)
                lst1 = ["\\None"]
                return lst1 + word3
    except Exception:
        return ["ERROR", "Sorry, \"{}\" is unavailable in database. [ :(  ]".format(word1), "Please try again."]