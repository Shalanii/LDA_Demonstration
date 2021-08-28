import argparse
import csv
from utils import *
from nltk.corpus import stopwords
from data_clean import Data_clean

def read_csv_file(original_file,cleaned_file):
    vocab = {}
    labels = []
    with open(original_file, 'r', newline='',encoding="ISO-8859-1") as file1:
        with open(cleaned_file, 'w', newline='',encoding="ISO-8859-1") as file2:
            data = csv.reader(file1)
            count = 0
            for row in data:
                count+=1
                x =row[0].strip()
                x = x.replace('\ufeff','')
                x = x.replace('\ufffd', '')
                cleaning = Data_clean()

                txt = cleaning.cleaner(row[1])
                txt = ' '.join(word for word in txt.split(' ') if not word.startswith("http"))

                if txt != "":
                    labels.append(int(x))
                #txt = row[1]
                    file2.write(txt+"\n")
                    arr = re.split('\s', txt[:-1])
                    filtered_words = [word for word in arr if word not in stopwords.words('english')]
                    for wd in filtered_words:
                        try:
                            vocab[wd] += 1
                        except:
                            vocab[wd] = 1
    return vocab,labels

dataset = "health"
parser = argparse.ArgumentParser()
parser.add_argument('--cleaned_file', default=dataset+'/cleaned-data.csv', help='input text file')
parser.add_argument('--text_file', default=dataset+'/'+dataset+'.csv', help='input text file')
parser.add_argument('--corpus_file', default=dataset+'/doc_term_mat.txt', help='term document matrix file')
parser.add_argument('--vocab_file', default=dataset+'/vocab.txt', help='vocab file')
parser.add_argument('--vocab_max_size', type=int, default=15000, help='maximum vocabulary size')
parser.add_argument('--vocab_min_count', type=int, default=3, help='minimum frequency of the words')
args = parser.parse_args()

# create vocabulary
print('create vocab')
vocab,labels = read_csv_file(args.text_file,args.cleaned_file)

vocab_arr = [[wd, vocab[wd]] for wd in vocab if vocab[wd] > args.vocab_min_count]
vocab_arr = sorted(vocab_arr, key=lambda k: k[1])[::-1]
vocab_arr = vocab_arr[:args.vocab_max_size]
vocab_arr = sorted(vocab_arr)

fout = open(args.vocab_file, 'w', encoding="ISO-8859-1")
for itm in vocab_arr:
    itm[1] = str(itm[1])
    fout.write(' '.join(itm)+'\n')
fout.close()

# vocabulary to id
vocab2id = {itm[1][0]: itm[0] for itm in enumerate(vocab_arr)}
print('create document term matrix')
data_arr = []
fp = open(args.cleaned_file, 'r',encoding="ISO-8859-1")
fout = open(args.corpus_file, 'w',encoding="ISO-8859-1")
for line in fp:
    arr = re.split('\s', line[:-1])
    arr = [str(vocab2id[wd]) for wd in arr if wd in vocab2id]
    sen = ' '.join(arr)
    fout.write(sen+'\n')
fp.close()
fout.close()

with open(dataset+'/original_labels.txt', 'w') as f:
    for item in labels:
        f.write(str(item)+"\n")

