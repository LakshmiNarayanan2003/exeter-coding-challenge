import pandas as pd
import re
import csv
import os, psutil
import time


def translateToFrench(csvFile, wordFile, textFile):
    wordDictionary = {}
    countDictionary = []
    csvData = pd.read_csv(csvFile, header=None)
    with open(wordFile, 'r') as file:
        data = file.read()
        words = data.split()
        for i in range(len(words)):
            for index, row in csvData.iterrows():
                if row[0].lower() == words[i].lower():
                    wordDictionary.update({words[i]: row[1]})
                    countDictionary.append({"English": words[i], "French": row[1], "Count": 0})
                    words[i] = row[1]

    with open(textFile, 'r') as txtF:
        txtData = txtF.read()
        txt = txtData.split()
        for i in range(len(txt)):
            for j in range(len(countDictionary)):
                char_txt = re.sub(r"[^a-zA-Z0-9 ]", "", txt[i])
                if char_txt.lower() == countDictionary[j]["English"].lower():
                    txt[i] = countDictionary[j]['French'] + " "
                    countDictionary[j]['Count'] += 1

    with open('t8.shakespeare.translated.txt', 'w') as frenchT:
        for i in txt:
            frenchT.write(i + " ")

    csv_columns = ['English', 'French', 'Count']
    try:
        with open("frequency.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in countDictionary:
                writer.writerow(data)
    except IOError:
        print("I/O error")

    with open('performance.txt', 'w') as perfp:
        memorySize = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)
        perfp.write('Time to process: %f'%(time.time() - start_time)+ ' Seconds\nMemory used: ' + str(memorySize)+" MB")


start_time = time.time()
translateToFrench('files/french_dictionary.csv', 'files/find_words.txt', 'files/t8shakespeare.txt')

# Algorithm
# 1) Translate all words in find_words.txt from English to French
# 2) Translate the t8shakespeare.txt
# 3) Count of translated words
# 4) Time taken
# 5) Memory
