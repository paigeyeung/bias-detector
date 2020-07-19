import csv
import pandas as pd
import nltk 
from nltk.corpus import stopwords 
import re, string
import heapq 
from goose3 import Goose
from collections import Counter

print("1")
nltk.download('wordnet')
nltk.download('stopwords') #get stop words
nltk.download('punkt')
stop_words = stopwords.words('english')
lemmatizer = nltk.wordnet.WordNetLemmatizer()
print("2")

def buildFile(fileName):
	g = Goose()
	biased = list() #list of news articles labeled "Opinion"
	fair = list() #list of news articles labeled "News"
	other =list() #list of news articles labeled "Other"
	data = open(fileName)
	rd = csv.reader(data, delimiter="\t", quotechar='"')
	for row in rd: 
	  if row[1] == "Opinion":
		  biased.append(row[0])
	  elif row[1] == "News":
		  fair.append(row[0])
	  else:
		  other.append(row[0])

	biased = biased[:100]
	fair = fair[:100]
	print("3")

	#bias
	biasText = ""
	for url in biased:
	  try:
		  print("3.1")
		  biasText += g.extract(url=url).cleaned_text
		  print("3.2")
	  except:
		  print("can't load article " + url)

	print("4")

	#fair
	fairText = ""
	for url in fair:
	  try:
		  print("4.1")
		  fairText += g.extract(url=url).cleaned_text
		  print("4.2")
	  except:
		  print("can't load article " + url)

	print("5")

	#tokenize the biasText
	store_tokens = open('bias.txt', 'w')
	dataset = nltk.sent_tokenize(biasText)
	for word in dataset: 
		word = word.lower() 
		word = re.sub(r'\W', ' ', word) 
		word = re.sub(r'\s+', ' ', word)
		word = lemmatizer.lemmatize(word)
		if ((len(word) > 0) and (word not in string.punctuation) and (word not in stop_words)):
		  store_tokens.write(word)
	store_tokens.close()

	print("6")
	#tokenize the fairText
	store_tokens = open('neutral.txt', 'w')
	fairdata = nltk.sent_tokenize(fairText) 
	for word in fairdata: 
		word = word.lower() 
		word = re.sub(r'\W', ' ', word) 
		word = re.sub(r'\s+', ' ', word)
		word = lemmatizer.lemmatize(word)
		if len(word) > 0 and word not in string.punctuation and word not in stop_words:
		  store_tokens.write(word)
	store_tokens.close()

	print("7")
	#getting specific words that are "biased"
	biasedWords = []
	store_tokens = open('exclusive-bias.txt', 'w')
	for word in data:
		if word in dataset and word not in fairdata:
		  biasedWords.append(word)
	if len(word) > 0 and word not in string.punctuation and word not in stop_words:
		store_tokens.write(word)
	store_tokens.close()


buildFile("newsArticlesWithLabels.tsv")

print("8")
#tokenize the tweet
tweet = input("Enter your tweet here: ")
twtData = nltk.sent_tokenize(tweet) 
for word in twtData: 
    word = word.lower() 
    word = re.sub(r'\W', ' ', word) 
    word = re.sub(r'\s+', ' ', word)


b = open("exclusive-bias.txt")
biasedFile = b.read()
biasedFile = biasedFile.split()

print("9")
#check for bias (counter)
bias = 0
for l in twtData:
	if l in biasedFile:
		bias += 1


print("10")
#bias meter (temporary solution)
countlength = tweet.split()
length = len(countlength)

percentbias = bias/length*100

try:
  userpercent = int(input("Enter the percent of biased words in a particular article for you to deem it biased (from 1 to 100)"))
except:
  userpercent = int(input("Your input is not a number, try again: "))

if percentbias > userpercent: 
	print("Most likely contains bias")
else:
	print("May contain bias, but below user percentage")
