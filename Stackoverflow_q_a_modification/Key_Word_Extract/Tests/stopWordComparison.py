from nltk.corpus import stopwords

stoppath = "SmartStoplist.txt"

stop_words = set(stopwords.words('english'))
# print stop_words


with open("SmartStoplist.txt", 'r') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

new = set(content)

print sorted(stop_words.difference(new.intersection(stop_words)))
