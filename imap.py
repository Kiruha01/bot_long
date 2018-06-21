from imbox import Imbox
mail = 'liss-2001g@mail.ru'

def check():
    with Imbox('imap.yandex.ru',
                username='kirill.lisoff2017',
                password='316011kirill',
                ssl=True) as imbox:
        messages = imbox.messages(unread=True)
        if messages:
            data = []
            for uid, message in messages:
                if message.sent_from[0]['email'] == mail:
                    print(1)
                    text = message.body['plain'][0].split()
                    for i in text:
                        print(i)
                        if 'examer.ru' in i:
                            data.append(i)
                imbox.mark_seen(uid)
            return data

