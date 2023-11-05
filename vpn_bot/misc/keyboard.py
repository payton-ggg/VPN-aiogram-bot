import aiogram

#Клавиатура меню Для админов
def main_admin_markup():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🛒Купить конфиг', '🚩Профиль')
    keyboard.row('📖Правила проекта', '🆘Поддержка')
    keyboard.row('👑Админка')
    return keyboard

#Кнопка обратно
def back_markup():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🔙Обратно')
    return keyboard

#Клавиатура админ меню
def admin_keyboard():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📬Рассылка', '📈Статистика')
    keyboard.row('➕Добавить промокод', '✏️Управление промокодами')
    keyboard.row('✏️Управление пользователями', '🥶Управление админами') 
    keyboard.row('🧪Управление проектом')
    keyboard.row('🔙Назад')
    return keyboard
#Настройки конфига
def settings():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("💱Изменить цену")
    keyboard.row('🔙Назад')
    return keyboard
#Управление серверами
def server_control_markup():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("➕Добавить сервер","📝Список серверов")
    keyboard.row('🔙Обратно')
    return keyboard
#Управоение проектом
def project_control():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("⚙Настройка", "📶Управление серверами")
    keyboard.row('🔙Обратно')
    return keyboard
#Управление админами
def edit_admins():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🤩Выдать админку', '😠Забрать админку')
    keyboard.row('📜Список админов')
    keyboard.row('🔙Обратно')
    return keyboard
#Клавиатура меню Для юзеров
def main_user_markup():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🛒Купить конфиг', '🚩Профиль')
    keyboard.row('📖Правила проекта', '🆘Поддержка') 
    return keyboard
#Клавиатура выбора платежного сервиса
def payment_service_markup(summ,do):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('🔶Crystal Pay', callback_data=f"add_funds|crystal|{do}|{summ}"),
        aiogram.types.InlineKeyboardButton("🔶Lolz", callback_data=f"add_funds|lolz|{do}|{summ}"),
        aiogram.types.InlineKeyboardButton("🔶Qiwi", callback_data=f"add_funds|qiwi|{do}|{summ}")
    )
    return keyboard
#Клавиатура выбора товара
def product_choise_markup():
    keyboard = aiogram.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('📶Конфиг для OpenVpn', callback_data='ovpn')
        )
    return keyboard
#Клавиатура профиля
def profile_markup():
    keyboard = aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('⬆️Пополнить баланс', callback_data='add_funds|'),
        aiogram.types.InlineKeyboardButton('⬆️Активировать промокод', callback_data='act_prm'),
        aiogram.types.InlineKeyboardButton('🤖 API проекта', callback_data='api_menu')
    )
    return keyboard
#Клавиатура рассылки
def mailing_markup():
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('❌Отмена')
    return keyboard
#Клавиатура статистики
def statistics_keyboard():
    keyboard = aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('❌Обнулить статистику покупок', callback_data='clear_stat')
    )
    return keyboard
#Клавиатура выбора локации
def loc_choice_markup(data):
    keyboard = aiogram.types.InlineKeyboardMarkup(row_width=2)
    for i in data:
        keyboard.add(aiogram.types.InlineKeyboardButton(i[0], callback_data = f"byu_cfg|0|loc{i[1]}"))
    return keyboard
#Клавиатура выбора периода
def days_choice_markup(arg):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('🔷30 дней', callback_data=f"byu_cfg|1|{arg}|30|1"),
        aiogram.types.InlineKeyboardButton("🔷60 дней", callback_data=f"byu_cfg|1|{arg}|60|1.8"),
        aiogram.types.InlineKeyboardButton("🔷90 дней", callback_data=f"byu_cfg|1|{arg}|90|2.6")
    )
    return keyboard
#Клавиатура оплаты
def pay_markup(summ,loc,days):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('✅Оплатить', callback_data=f"byu_cfg|2|{summ}|{loc}|{days}"),
        aiogram.types.InlineKeyboardButton("❌Отменить оплату", callback_data="byu_cfg|3")
    )
    return keyboard
#Клавиатура пополнения Киви
def add_funds_qiwi_markup(url, id, summ):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('💳Оплатить', url=url),
        aiogram.types.InlineKeyboardButton("✅Проверить оплату", callback_data=f"add_funds|qiwi|1|{summ}|{id}"),
        aiogram.types.InlineKeyboardButton("🚫Отменить оплату", callback_data=f"add_funds|qiwi|2|{id}")
    )
    return keyboard
#Клавиатура пополнения Кристал пей
def add_funds_crystal_markup(new_bill,summ, id):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton('💳Оплатить', url=new_bill),
        aiogram.types.InlineKeyboardButton("✅Проверить оплату", callback_data=f"add_funds|crystal|1|{summ}|{id}")
    )
    return keyboard
#Клавиатура пополнения Лолз
def add_funds_lolz_markup(pay_url,comment,summ):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton("💳Оплатить", url=pay_url),
        aiogram.types.InlineKeyboardButton("✅Проверить оплату", callback_data=f"add_funds|lolz|1|{summ}|{comment}")
    )
    return keyboard
#Клавиатура удаления промокода
def delete_promo_markup(promo):
    keyboard=aiogram.types.InlineKeyboardMarkup()
    keyboard.add(
        aiogram.types.InlineKeyboardButton("❌Удалить", callback_data=f"do_prm|delete|{promo}")
    )
    return keyboard
#Клавиатура изменения баланса юзера
def change_user_balance_markup(user):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton("🤑Изменить баланс", callback_data=f"change_bal|{user}"),
        aiogram.types.InlineKeyboardButton("😈Заблокировать", callback_data=f"block|{user}"),
        aiogram.types.InlineKeyboardButton("😇Разблокировать", callback_data=f"unb_lock|{user}")
    )
    return keyboard
#Клавиатура поддержки
def help_markup(id):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton("😉Ответить", callback_data=f"help|{id}"),
        aiogram.types.InlineKeyboardButton("😒Проигнорировать", callback_data=f"ignor|{id}"),
        aiogram.types.InlineKeyboardButton("😈Заблокировать", callback_data=f"block|{id}")
    )
    return keyboard
#Удаление сервера
def delete_server_markup(server):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton("➖Удалить", callback_data=f"del_server|{server}")
    )
    return keyboard
#Апи меню
def api_menu(userid, docs_url):
    keyboard=aiogram.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        aiogram.types.InlineKeyboardButton("🔑 Генерировать ключ", callback_data=f"api_do|gen|{userid}"), 
        aiogram.types.InlineKeyboardButton("⚠ Отозвать ключ", callback_data=f"api_do|del|{userid}"),
        aiogram.types.InlineKeyboardButton("📔 Документация", url=docs_url)
    )
    return keyboard