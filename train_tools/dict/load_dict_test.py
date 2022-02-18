import pickle

<<<<<<< HEAD
f = open("./chatbot_dict1.bin", "rb")
=======
f = open("chatbot_dict.bin", "rb")
>>>>>>> d5dd420241fb34fedabd8bf69b5b576c627a15a3
word_index = pickle.load(f)
f.close()

print(word_index['OOV'])
<<<<<<< HEAD
print(word_index['cgv'])
print(word_index['상영표'])
=======
print(word_index['오늘'])
print(word_index['주문'])
print(word_index['삼선볶음밥'])
print(word_index['1시'])
>>>>>>> d5dd420241fb34fedabd8bf69b5b576c627a15a3
