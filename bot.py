import telebot
import keyboard
import config
from announcment import Announcement
import db

bot = telebot.TeleBot(config.token)

# When bot starts
@bot.message_handler(commands=["start"])
def sayHi(message):
    db.set_state(message.chat.id, config.States.S_START.value)
    state = db.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_CATEGORY.value:
        bot.send_message(message.chat.id, "Ожидаю выбора категории:)", reply_markup=keyboard.categoriesListKeyboard())
    elif state == config.States.S_ENTER_CITY.value:
        bot.send_message(message.chat.id, "Ожидаю ваш город:)")
    elif state == config.States.S_SEND_TITLE.value:
        bot.send_message(message.chat.id, "Ожидаю ваш заголовок:)")
    elif state == config.States.S_SEND_DESCRIPTION.value:
        bot.send_message(message.chat.id, "Ожидаю ваше описание:)")
    elif state == config.States.S_SEND_PRICE.value:
        bot.send_message(message.chat.id, "Ожидаю вашу цены на товар:)") 
    elif state == config.States.S_SEND_PHOTO.value:
        bot.send_message(message.chat.id, "Ожидаю фото товара:)")     
    else:
        bot.send_message(message.chat.id, "Рад встрече, чего желаете?", reply_markup=keyboard.menuKeyboard())
        db.set_state(message.chat.id, config.States.S_START.value)


# Questions flow
@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_ENTER_CATEGORY.value)
def user_entering_category(message):
    db.update_data(message.from_user.id, 'category', message.text)
    bot.send_message(message.chat.id, "Супер. Напишите ваш город:", reply_markup=keyboard.hideKeyboard())
    db.set_state(message.chat.id, config.States.S_ENTER_CITY.value)  

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_ENTER_CITY.value)
def user_entering_city(message):
    if len(message.text) < 2 or len(message.text) > 30:
        bot.send_message(message.chat.id, "Введите настоящий город!")
        return
    else:
        db.update_data(message.from_user.id, 'city', message.text)
        bot.send_message(message.chat.id, "Хорошо, ваш заголовок:")
        db.set_state(message.chat.id, config.States.S_SEND_TITLE.value)

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_SEND_TITLE.value)
def user_entering_title(message):
    if len(message.text) < 3 or len(message.text) > 30:
        bot.send_message(message.chat.id, "Слишком короткое/длинное название!")
        return
    else:
        db.update_data(message.from_user.id, 'title', message.text)
        bot.send_message(message.chat.id, "Понял, теперь описание:")
        db.set_state(message.chat.id, config.States.S_SEND_DESCRIPTION.value)

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_SEND_DESCRIPTION.value)
def user_entering_description(message):
    if len(message.text) < 10 or len(message.text) > 255:
        bot.send_message(message.chat.id, "Слишком короткое/длинное описание!")
        return
    else:
        db.update_data(message.from_user.id, 'description', message.text)
        bot.send_message(message.chat.id, "Хорошо, введите цену (BYN):")
        db.set_state(message.chat.id, config.States.S_SEND_PRICE.value)

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_SEND_PRICE.value)
def user_entering_price(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Только цифры:)")
        return
    if int(message.text) < 1 or int(message.text) > 10000:
        bot.send_message(message.chat.id, "Введите нормальную цену:)")
        return
    else:
        db.update_data(message.from_user.id, 'price', message.text)
        bot.send_message(message.chat.id, "Пришлите мне одно фото товара")
        db.set_state(message.chat.id, config.States.S_SEND_PHOTO.value)

@bot.message_handler(content_types=["photo"], func=lambda message: db.get_current_state(message.chat.id) == config.States.S_SEND_PHOTO.value)
def user_sending_photo(message):
    contacts = "@{}".format(message.from_user.username)
    db.update_data(message.from_user.id, 'contacts', contacts)
    db.update_data(message.from_user.id, 'photo', message.photo[-1].file_id)
    result = db.fetch(message.from_user.id)
    announc = Announcement(result)
    bot.send_photo(message.chat.id, photo=announc.photo, caption="Поздравляю! Можете отправить объявление на модерацию.\n\n{}".format(announc.showInfo()), reply_markup=keyboard.endKeyboard(), parse_mode="Markdown")
    db.set_state(message.chat.id, config.States.S_START.value)

# Handle buttons commands
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "startConstructor":
        if (call.from_user.username is None):
            bot.send_message(call.message.chat.id, "В настройках укажите свой логин, чтобы с вами могли связаться покупатели и возвращайтесь! :)")
        else:
            bot.send_message(call.message.chat.id, "Выберите категорию: ", reply_markup=keyboard.categoriesListKeyboard())
            db.set_state(call.message.chat.id, config.States.S_ENTER_CATEGORY.value)
    elif call.data == "sendToModeration":
        result = db.fetch(call.from_user.id)
        announc = Announcement(result)
        bot.send_photo(config.admin_chat_id, photo=announc.photo, caption="Новое объявление!\n\n {}".format(announc.showInfo()), parse_mode="Markdown")
        bot.send_message(call.message.chat.id, "Отправлено на модерацию!")
    elif call.data == "help":
        bot.send_message(
            call.message.chat.id, "Я создан для того, чтобы помогать вам составлять объявления. Следуйте инструкциям, публикация после модерации.\nУ вас всё получится:)")

# Handle all text
@bot.message_handler(content_types="text")
def fillAnnouncement(message):
    bot.send_message(message.chat.id, "Не понимаю:)")