import pickle

f = open("./chatbot_dict1.bin", "rb")
word_index = pickle.load(f)
f.close()

print(word_index['OOV'])
print(word_index['cgv'])
print(word_index['상영표'])
