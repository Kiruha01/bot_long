token = 'e4276027b3dd1635f80f2e627bd085200e3018f51fa3cb5ce462797f1c420c32f082091a5560ba1bc5b38'
list_id = [] # Для уведомления после флуда
import vk_api
from vk_api import longpoll

from examer import Examer
from keyboard import convert_keyboard
from imap import check

vk = vk_api.vk_api.VkApi(token=token, api_version='5.80')
long = longpoll.VkLongPoll(vk)
ex = Examer('arkadiy@p33.org', 'zabylkto01')

memory = {}
keyboard = []
keyboard.append([["Обновить", "negative"]])
keyboard = convert_keyboard(keyboard)
print(keyboard)

def gen_keyboard(data):
    global keyboard
    keyboard = []
    this = []
    for index, value in enumerate(data):
        this.append([value, 'default'])
        if index % 3 == 2:
            keyboard.append(this)
            this = []
    if this:
        keyboard.append(this)
    keyboard.append([["Обновить", "negative"]])
    keyboard = convert_keyboard(keyboard)

def main(id, text):
    global memory
    global keyboard

    if list_id:
        for iii in list_id:
            vk.method('messages.send', {'user_id': iii, 'message': 'Сорян, меня забанили за флуд)\nТеперь всё ок'})

    if text == 'Начать':
        # this = []
        # for index, value in enumerate(memory):
        #     this.append([value, 'default'])
        #     if index % 3 == 2:
        #         keyboard.append(this)
        #         this = []
        # if this:
        #     keyboard.append(this)

        # keyboard.append([["Обновить", "negative"]])


        vk.method('messages.send', {'user_id': id, 'message': 'Кидай ссылку на тест и я решу его за тебя', 'keyboard': keyboard})

    elif text == 'Обновить':
        if str(id) == '276820555':
            vk.method('messages.send', {'user_id': id, 'message': 'Как обновлять', 'keyboard': convert_keyboard([[["По юзерам", "positive"], ["На почте!.", "primary"]]], True)})
        else:
            vk.method('messages.send', {'user_id': id, 'message': 'Клавиатура обновлена', 'keyboard': keyboard})
    elif text == 'reset' and str(id) == '276820555':
        memory = {}
        vk.method('messages.send', {'user_id': '276820555', 'message': 'ok'})
        print('||| ok')
    elif text == 'На почте!.':
        got = check()
        if got:

            gen_keyboard(list(memory.keys()) + got)
            vk.method('messages.send', {'user_id': id, 'message': 'Клавиатура обновлена', 'keyboard': keyboard})
        else:
            vk.method('messages.send', {'user_id': id, 'message': 'Нечего обновлять', 'keyboard': keyboard})
    elif text == 'По юзерам':
        vk.method('messages.send', {'user_id': id, 'message': 'Клавиатура обновлена', 'keyboard': keyboard})


    else:               # Значит кидают ссылку
        link = text.split('/')[-1]
        if link in memory:
            print('Read from memory')
            for msg in memory[link]:
                vk.method('messages.send', {'user_id': id, 'message': msg})
            vk.method('messages.send', {'user_id': id, 'message': 'Всё!', 'keyboard': keyboard})
            ex.list_of_task = []
        else:
            ex.set_link(text)
            try:
                ex.start()
            except ArithmeticError:
                vk.method('messages.send', {'user_id': id, 'message': 'Invalid Link'})
            else:
                ex.format_text()
                list_ = []
                for task_id in ex.list_of_task:
                    list_.append(task_id['question'] + '\nОтвет: ' + task_id['answer'])
                memory[link] = list_

                gen_keyboard(memory)

                main(id, text)
    



if __name__ == '__main__':
    from time import sleep


    for event in long.listen():
        if event.text and not event.from_me:
            try:
                main(event.user_id, event.text)
            except:
                list_id.append(event.user_id)
