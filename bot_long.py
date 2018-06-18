token = 'e4276027b3dd1635f80f2e627bd085200e3018f51fa3cb5ce462797f1c420c32f082091a5560ba1bc5b38'

import vk_api
from vk_api import longpoll
from examer import Examer

vk = vk_api.vk_api.VkApi(token=token)
long = longpoll.VkLongPoll(vk)
ex = Examer('arkadiy@p33.org', 'zabylkto01')

memory = {}

def main(id, text):
    global memory
    if text == 'Привет':
        vk.method('messages.send', {'user_id': id, 'message': 'Кидай ссылку на тест и я решу его за тебя'})
    elif text == 'reset' and str(id) == '276820555':
        memory = {}
        vk.method('messages.send', {'user_id': '276820555', 'message': 'ok'})
    else:
        link = text.split('/')[-1]
        if link in memory:
            for msg in memory[link]:
                vk.method('messages.send', {'user_id': id, 'message': msg})
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
                main(id, text)
    



if __name__ == '__main__':
    for event in long.listen():
        if event.text and not event.from_me:
            main(event.user_id, event.text)
