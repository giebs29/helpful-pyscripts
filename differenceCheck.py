from difflib import SequenceMatcher

string1 = "sA"
string2 = "sa"

ratio = SequenceMatcher(None,string1,string2).ratio()

print ratio
