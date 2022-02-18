import pandas as pd

df = pd.read_excel('종류규칙답변.xlsx')

rules = {}
row=0
for rule in df['r']:
    rules[row] = rule.split('|')
    row+=1

def chat(request):
    for k, v in rules.items():
        chat_flag = False
        for word in v:
            if word in request:
                chat_flag = True 
            else:
                chat_flag = False
                break
    if chat_flag:
        return df['a'][k]
    return '무슨 말인지 모르겠어요'

while True:
    user = input('\n안녕하세요! 무엇이 궁금하신가요?\n>>>')
    if user == 'q':
        print('다음에봐요')
        break
    else:
        print(chat(user))
