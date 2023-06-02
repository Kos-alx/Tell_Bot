# t.me/echonew_11bot
'''
За основу взять учебный бот.
Добавлены были следующие изменения:
1. Ответ округляется до двух заков после точки.
2. При выводе валюты учитывается окончание. 1 рубль, 3 рубля, 5 рублей. Определяется это в словаре в файле config.py
3. Теперь не обязательно название валюты указывать полностью, достаточно одной или нескольких первых букв.
Программа будет искать совпадает ли начало валюты с полным название.
Запрос: <дол евр 2> выдаст Цена 2 долларов составит 1.86 евро
Запрос: <д е 2> выдаст такой же ответ.
Запрос: <дл евр 2> выдаст ошибку: Не удалось обработать валюту дл

'''

# HTTP API: 6244436216:AAH0-z5qw-ktT2-H5MJsT8v53zbsvYw0KNg


import telebot
from extensions import APIException, CryptoConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Должно быть три параметра:\n'
                                      '<валюта из которой хотите перевести>\n'
                                      '<валюта в которую хотите перевести>\n'
                                      '<количество>')
        quote, base, amount = values
        amount, quote, total_base, base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        amount, quote, total_base, base = CryptoConverter.end_change(amount, quote, total_base, base)
        text = f'Цена {amount} {quote} составит {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)