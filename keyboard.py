from telebot import types

def menuKeyboard():
    keyboard = types.InlineKeyboardMarkup(1.0)
    start_button = types.InlineKeyboardButton(text="Составить объявление", callback_data="startConstructor")
    help_button = types.InlineKeyboardButton(text="Помощь", callback_data="help", )
    contact_button = types.InlineKeyboardButton(text="Связь с админом", url="http://t.me/FlexonZ")
    keyboard.add(start_button, contact_button, help_button)

    return keyboard

def endKeyboard():
    keyboard = types.InlineKeyboardMarkup(2.0)
    send_button = types.InlineKeyboardButton(text="Опубликовать", callback_data="sendToModeration")
    new_button = types.InlineKeyboardButton(text="Создать новое", callback_data="startConstructor")
    help_button = types.InlineKeyboardButton(text="Помощь", callback_data="help", )
    contact_button = types.InlineKeyboardButton(text="Связь с админом", url="http://t.me/FlexonZ")
    keyboard.add(send_button, new_button, help_button, contact_button)

    return keyboard

def categoriesListKeyboard():
    keyboard = types.ReplyKeyboardMarkup(4.0)
    kids_button = types.KeyboardButton("🧒#Дети")
    comsetics_button = types.KeyboardButton("👛#Косметика")
    tech_button = types.KeyboardButton("📱#Техника")
    home_button = types.KeyboardButton("🛋#Дом")
    clothes_button = types.KeyboardButton("👕#Одежда")
    zoo_button = types.KeyboardButton("🐣#Зоо")
    sport_button = types.KeyboardButton("⚽️#Спорт")
    gifts_button = types.KeyboardButton("🧧#Сувенир")
    keyboard.add(kids_button, comsetics_button, tech_button, home_button,
                 clothes_button, zoo_button, sport_button, gifts_button)

    return keyboard

def hideKeyboard():
    return types.ReplyKeyboardRemove()