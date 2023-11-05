#Глобальные импорты
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
from aiogram import types

#Локальные импорты
from misc import config, misc
from misc import database as db
from misc import keyboard as kb

#Импорты систем оплаты
from pycrystalpay import CrystalPay
from payment import lolzapi
from pyqiwip2p import AioQiwiP2P

storage = MemoryStorage()
bot=Bot(config.bot_token, parse_mode=types.ParseMode.HTML)
dp=Dispatcher(bot, storage=storage)

lolz = lolzapi.LolzteamApi(config.lolz_api[0], config.lolz_api[1])
crystal_pay = CrystalPay(config.crystal_pay[0],config.crystal_pay[1])
p2p = AioQiwiP2P(auth_key=config.qiwi_key)

db.create_tables()
misc.clear()

#Объявления стейтов
class st(StatesGroup):
    users_control_input = State()

    new_admin_id_input = State()
    cancell_admin = State()

    help_user = State()
    help_admin = State()

    mailing = State()

    act_promo = State()

    add_promo_p1 = State()
    add_promo_p2 = State()
    add_promo_p3 = State()

    add_funds = State()

    settings = State()

    add_server_p1 = State()
    add_server_p2 = State()

    change_bal = State()

#Реакция на старт
@dp.message_handler(commands=["start"], chat_type=["private"])
async def star(message: types.Message):
    cmd=message.text.split()
    try:
        if len(cmd) == 1:
            if await db.get_user_info(message.chat.id) is None:
                await db.save_user_info(message.chat.id)
        elif len(cmd) == 2:
            if await db.get_user_info(message.chat.id) is None:
                await db.save_user_info(message.chat.id,cmd[1])
                await bot.send_message(cmd[1], f"@{message.from_user.username} твой новый реферал.😍")
    except: pass
    else:
        blocked= await db.get_user_info(int(message.from_user.id)); blocked=blocked[5]
        if not blocked:
            adm = await db.get_user_info(message.chat.id)
            if adm[4]: await message.answer(f'🤝Добро пожаловать, <b>{message.from_user.first_name}</b> слит в @end_soft', reply_markup=kb.main_admin_markup())
            else: await message.answer(f'🤝Добро пожаловать, <b>{message.from_user.first_name}</b> слит в @end_soft', reply_markup=kb.main_user_markup())
        else: await message.answer("<b>Ты забанен и не можешь использовать функции этого бота.</b> слит в @end_soft") 

#Хендлер калл-даты
@dp.callback_query_handler()
async def close_update(call: types.CallbackQuery, state: FSMContext):
    try: 
        if "add_funds" not in call.data: await call.message.delete()
    except: 
        pass
    #Админ функции
    if "ignor" in call.data:
        raw = call.data.split("|")
        await call.message.answer("<b>👎 Проигнорировано</b>")
        await bot.send_message(raw[1], "<b>❗ Ваше обращение было отклонено. Попробуйте обьяснить свою проблему более детально.</b>")
    elif "block" in call.data:
        raw = call.data.split("|")
        await db.ban(raw[1], 1)
        await call.message.answer("👍<b> Забанил</b>")
        await bot.send_message(raw[1], "😡<b> Ты был забанен</b>")
    elif "help" in call.data:
        raw = call.data.split("|")
        await call.message.answer("<b>✍ Напишите свой ответ для ответа юзеру</b>")
        await st.help_admin.set()
        await state.update_data(padmin=call.from_user.id)
        await state.update_data(uid=raw[1])
    elif "unb_lock" in call.data:
        raw = call.data.split("|")
        user_info = await db.get_user_info(raw[1])
        if user_info[5]:
            await db.ban(raw[1], 0)
            await call.message.answer("👍<b> Разбанил</b>")
            await bot.send_message(raw[1], "<b>😘 Ты был разблокирован</b>")
        else:
            await call.message.answer("❕ <b>Этот пользователь не забанен</b>")
    elif "promo" in call.data:
        raw = call.data.split("|")
        promo_info = await db.get_promo_info(raw[1])
        text = f"Id: {promo_info[0]}\nПромокод: {promo_info[1]}\nСумма: {promo_info[2]}\nКолличество активаций: {promo_info[3]}"
        await call.message.answer(text, reply_markup=kb.delete_promo_markup(raw[1]))
    elif "do_prm" in call.data:
        raw = call.data.split("|")
        promo = raw[2]
        do=raw[1]
        match do:
            case "delete":
                await db.delete_promo(promo)
                await call.message.answer(f"Готово, промокод <b>{promo}</b> удален.")
    elif "server_info" in call.data:
        raw = call.data.split("|")
        info = await db.get_server(int(raw[1]))
        text = f"🆔Id: {info[0]}\n📛Название: {info[1]}\n☁Ip: {info[2]}"
        await call.message.answer(text,reply_markup=kb.delete_server_markup(raw[1]))
    elif "del_server" in call.data:
        raw = call.data.split("|")
        server_info = await db.get_server(int(raw[1]))
        await db.delete_server(int(raw[1]))
        await call.message.answer(f"✅Успешно, сервер <b>{server_info[1]}</b> удален.")
    elif "change_bal" in call.data:
        row = call.data.split("|")
        await call.message.answer("Введи баланс")
        await st.change_bal.set()
        await state.update_data(case=row[1])
    elif "clear_stat" in call.data:
        await db.clear_stat()
        await call.message.answer("✅<b>Статистика очищенна.</b>")

    #Пользовательские обработки
    if "act_prm" in call.data:
        await call.message.answer("Введите промокод")
        await st.act_promo.set()
    elif "api_menu" in call.data:
        api_key = await db.get_user_info(call.from_user.id); api_key=str(api_key[6]).replace("None", "Отсутствует")
        text=f'⚙ <b>Меню управления API</b>\n🔻Ваш ключ: <span class="tg-spoiler"><b>{api_key}</b></span>'
        await call.message.answer(text,reply_markup=kb.api_menu(call.from_user.id, "https://google.com"))
    elif "api_do" in call.data:
        raw=call.data.split("|")
        do=raw[1]
        data=raw[2]
        match do:
            case "gen":
                key=misc.generate_api_key()
                await db.update_key(call.from_user.id, key)
                await call.message.answer(f'<i>Готово, ваш ключ API:</i> <span class="tg-spoiler"><b>{key}</b></span>')
            case "del":
                await db.update_key(call.from_user.id)
                await call.message.answer("<b>✅ Готово, ваш API-ключ сброшен, получить новый можно в меню.</b>")
    elif "add_funds" in call.data:
        raw = call.data.split("|")
        match raw[1]:
            case "":
                await call.message.delete()
                await call.message.answer("💰 <i>Введи сумму.</i>")
                await st.add_funds.set()
            case "qiwi":
                match raw[2]:
                    case "0":
                        await call.message.delete()
                        summ = int(raw[3])
                        bill = await p2p.bill(amount=summ, lifetime=20)
                        await call.message.answer("🥝 <i>Пополнение киви</i>", reply_markup=kb.add_funds_qiwi_markup(bill.pay_url, bill.bill_id, summ))
                    case "1":
                        id = raw[4]
                        summ = raw[3]
                        status = await p2p.check(bill_id=id); status = status.status
                        if status == "PAID":
                            await call.message.delete()
                            await call.message.answer(f"✅Успешно, ваш платеж найден, баланс пополнен на {misc.beauty_int(summ)} RUB.")
                            balance = await db.get_user_info(call.from_user.id); balance = balance[1]
                            new_balance = int(summ) + balance
                            await db.write_balance(new_balance, call.from_user.id)
                            inviter = await db.get_inviter(call.message.from_user.id)
                            if inviter != None:
                                inviter_bal = await db.get_user_info(inviter)
                                percentage = float(summ)/float(10)
                                new_inviter_bal=inviter_bal[1]+percentage
                                await db.write_balance(round(new_inviter_bal), inviter)
                                await bot.send_message(inviter, f"Твой реферал👤, совершил покупку🛒.\nТвой процент: {misc.beauty_int(round(percentage))}\nНовый баланс: <b>{misc.beauty_int(round(new_inviter_bal))}</b>")
                        else:
                            await bot.answer_callback_query(call.id, "Простите🙏, но ваш платеж не был найден❌, если вы оплатили и платежа не обнаружено, пишите в Техподдержку.", show_alert=True)
                    case "2":
                        await call.message.delete()
                        id = raw[3]
                        await p2p.reject(bill_id=id)
                        await call.message.answer("❌ <b>Счет отменен</b>")
            case "crystal":
                match raw[2]:
                    case "0":
                        await call.message.delete()
                        summ = int(raw[3])
                        new_bill = crystal_pay.create_invoice(summ)
                        await call.message.answer("🔮 <i>Пополнение кристал пей</i>", reply_markup=kb.add_funds_crystal_markup(new_bill.url, summ, new_bill.id))
                    case "1":
                        summ = raw[3]
                        status=crystal_pay.construct_payment_by_id(raw[4]).if_paid()
                        if status:
                            await call.message.delete()
                            await call.message.answer(f"✅ <b>Успешно!</b> Ваш платеж найден, баланс пополнен на {misc.beauty_int(summ)} RUB.")
                            balance = await db.get_user_info(call.from_user.id); balance = balance[1]
                            new_balance = int(summ) + balance
                            await db.write_balance(new_balance, call.from_user.id)
                            inviter = await db.get_inviter(call.message.chat.id)
                            if inviter != None:
                                inviter_bal = await db.get_user_info(inviter)
                                percentage = float(summ)/float(10)
                                new_inviter_bal=inviter_bal[1]+percentage
                                await db.write_balance(round(new_inviter_bal), inviter)
                                await bot.send_message(inviter, f"Твой реферал👤, совершил покупку🛒.\nТвой процент: {misc.beauty_int(round(percentage))}\nНовый баланс: <b>{misc.beauty_int(round(new_inviter_bal))}</b>")
                        else:
                            await bot.answer_callback_query(call.id, "Простите🙏, но ваш платеж не был найден❌, если вы оплатили и платежа не обнаружено, пишите в Техподдержку.", show_alert=True)
            case "lolz":
                match raw[2]:
                    case "0":
                        comment = misc.comment_generation(call.message.from_user.id)
                        await call.message.delete()
                        pay_url=f"https://lolz.guru/market/balance/transfer?username={config.lolz_api[2]}&amount={raw[3]}&comment={comment}"
                        await call.message.answer("Перевод средств доступен по ссылке ниже!\n<b>Важно!</b>\n<i>При указании неверной суммы, либо неверного комментария, баланс не будет пополнен.</i>", reply_markup=kb.add_funds_lolz_markup(pay_url, comment, raw[3]))
                    case "1":
                        summ = int(raw[3])
                        comment = raw[4]
                        check_paym=lolz.market_payments(type_='income', pmin=comment, pmax=comment, comment=comment)["payments"]
                        if check_paym:
                            await call.message.delete()
                            await call.message.answer(f"✅ Успешно, ваш платеж найден, баланс пополнен на <b>{misc.beauty_int(summ)} RUB</b>.")
                            balance = await db.get_user_info(call.from_user.id); balance = balance[1]
                            new_balance = summ + balance
                            await db.write_balance(new_balance, call.from_user.id)
                            inviter = await db.get_inviter(call.message.chat.id)
                            if inviter != None:
                                inviter_bal = await db.get_user_info(inviter)
                                percentage = float(summ)/float(10)
                                new_inviter_bal=inviter_bal[1]+percentage
                                await db.write_balance(round(new_inviter_bal), inviter)
                                await bot.send_message(inviter, f"Твой реферал👤, совершил покупку🛒.\nТвой процент: {misc.beauty_int(round(percentage))}\nНовый баланс: <b>{misc.beauty_int(round(new_inviter_bal))}</b>")
                        else:
                            await bot.answer_callback_query(call.id, "Простите🙏, но ваш платеж не был найден❌, если вы оплатили и платежа не обнаружено, пишите в Техподдержку.", show_alert=True)
    elif "byu_cfg" in call.data:
        raw = call.data.split("|")
        match raw[1]:
            case "0":
                await call.message.answer("<i>📅 Выберите период</i>...", reply_markup=kb.days_choice_markup(raw[2]))
            case "1":
                one_cfg_summ = await db.get_one_summ()
                summ = (float(raw[4])) * one_cfg_summ
                loc = await db.get_server(raw[2].replace("loc", "")); loc = loc[1]
                balance = await db.get_user_info(int(call.from_user.id)); balance = balance[1]
                await call.message.answer(f"Локация: {loc}\nСумма: {misc.beauty_int(int(summ))} RUB\nПериод: {raw[3]} Дней\nБаланс: <b>{misc.beauty_int(balance)} RUB</b>",reply_markup=kb.pay_markup(int(summ), raw[2], raw[3]))
            case "2":
                loc = await db.get_server(raw[3].replace("loc", ""))
                summ = int(raw[2])
                period = raw[4]
                balance = await db.get_user_info(call.from_user.id); balance = balance[1]
                if balance >= summ:
                    await db.write_payment_info(summ, call.from_user.id, raw[3])
                    await call.message.answer("✅Успешно, ожидайте генерации конфига.")
                    new_bal = balance - summ
                    await db.write_balance(new_bal, call.from_user.id)
                    file=misc.generate_config(call.from_user.id, period, loc).split("/")[2]
                    otzv = types.InlineKeyboardMarkup()
                    otzv.add(types.InlineKeyboardButton("Написать отзыв", url=config.lolz_theme))
                    await call.message.answer_document(open(file, "rb"), caption="✅Успешно\nПриветствую, дорогой покупатель! Если вы читаете эту инструкцию то вы однозначно заинтересовались нашим товаром.\n\n<i>Инструкция сделана для людей которые не знают как использовать конфигурации для клиента OpenVpn.</i>\n1)Скачайте клиент OpenVpn - https://openvpn.net/community-downloads/\n2)Установите клиент OpenVpn\n3)Нажмите на ваш трей (стрелочка, в правом нижнем углу), выберете значек OpenVpn, далее пункт Импорт - импорт файла конфигурации, после чего кликните дважды на файл который только что купили.\nПосле чего нажмите подключится.\nBingo!, впн успешно настроен и работает!",reply_markup=otzv)
                    misc.delete(file)
                else:
                    na = summ - balance
                    await call.message.answer(f"❌У вас не хватает средств, пополните баланс на <b>{misc.beauty_int(na)} RUB</b>", reply_markup=kb.profile_markup())
#Обработчик текстовых кнопок
@dp.message_handler(content_types=["text"], chat_type=["private"])
async def text(message: types.Message, state: FSMContext):
    adm = await db.get_user_info(message.chat.id)
    if not adm[5]:
        #Админ функции
        if ("Админка" in message.text) and (adm[4]):
            await message.answer("👑Админ панель", reply_markup=kb.admin_keyboard())
        elif ("Назад" in message.text) and (adm[4]):
            await message.answer(f'🤝Добро пожаловать <b>{message.from_user.first_name}</b>', reply_markup=kb.main_admin_markup())
        elif ("Статистика" in message.text) and (adm[4]):
            users = await db.count_all_users()
            byus = await db.count_buys()
            pay_summ=await db.payments_summ()
            servers = await db.get_servers()
            bs = ""
            for x in servers:
                buys = await db.count_where_buys(f"loc{x[0]}")
                bs+=f"{x[1]}(Покупок) - {buys}\n"
            text=f"📈Статистика\n👤Пользователей:{users}\n🧮Покупок(Все время):{byus}\n💰Сумма покупок(Все время):{misc.beauty_int(pay_summ)} RUB\n{bs}"
            await message.answer(text, reply_markup=kb.statistics_keyboard())
        elif ("Управление пользователями" in message.text) and (adm[4]):
            await message.answer("🆔 <b>Введите id пользователя.</b>", reply_markup=kb.back_markup())
            await st.users_control_input.set()
        elif ("Обратно" in message.text) and (adm[4]):
            await message.answer("👑 <b>Админ панель</b>", reply_markup=kb.admin_keyboard())
        elif ("Управление админами" in message.text) and (adm[4]):
            await message.answer("🗿 <b>Управление администраторами</b>", reply_markup=kb.edit_admins())
        elif ("Выдать админку" in message.text) and (adm[4]):
            await message.answer("🆔 <b>Введите id человека которому нужно выдать админку.</b>")
            await st.new_admin_id_input.set()
        elif ("Забрать админку" in message.text) and (adm[4]):
            await message.answer("🆔 <b>Введите id человека у которого нужно забрать админку.</b>")
            await st.cancell_admin.set()
        elif ("Список админов" in message.text) and adm[4]:
            text="Id - Баланс\n"
            admins=await db.admin_list()
            for i in admins:
                id=i[0]
                bal=i[1]
                text+=f"{id} - {bal}\n"
            await message.answer(text)
        elif ("Рассылка" in message.text) and (adm[4]):
            await message.answer("✏ <b>Введи текст для рассылки</b>", reply_markup=kb.back_markup())
            await st.mailing.set()
        elif ("Управление промокодами" in message.text) and adm[4]:
            all_promos = await db.get_all_promos()
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            if len(all_promos) > 0:
                for i in all_promos:
                    keyboard.add(
                        types.InlineKeyboardButton(f"┠{i[1]}", callback_data=f"promo|{i[1]}")
                        )
            else:
                keyboard.add(
                        types.InlineKeyboardButton("😢 Промокоды отсутствуют", callback_data=f"no_prms")
                        )
            await message.answer("🙊 <b>Выберите промокод:</b>", reply_markup=keyboard)
        elif ("Добавить промокод" in message.text) and adm[4]:
            await message.answer("🙈 <b>Введите название промокода:</b>")
            await st.add_promo_p1.set()
        elif ("Управление проектом" in message.text) and adm[4]:
            await message.answer("🧪 <b>Управление проектом</b>", reply_markup=kb.project_control())
        elif ("Управление серверами" in message.text) and adm[4]:
            await message.answer("📶 <b>Управление серверами</b>", reply_markup=kb.server_control_markup())##
        elif ("Настройка" in message.text) and adm[4]:
            await message.answer("⚙ <b>Выберите параметр для изменения</b>", reply_markup=kb.settings())##
        elif ("Изменить" in message.text) and adm[4]:
            raw = message.text.split()
            match raw[1]:
                case "цену":
                    await message.answer("🏦 <b>Введите новую цену.</b>")
                    await st.settings.set()
                    await state.update_data(case="price")
        elif ("Список серверов" in message.text) and adm[4]:
            servers = await db.get_servers()
            keyboard = types.InlineKeyboardMarkup()
            for i in servers:
                keyboard.add(types.InlineKeyboardButton(f"{i[1]}", callback_data=f"server_info|{i[0]}"))
            await message.answer("Список серверов", reply_markup=keyboard)
        elif ("Добавить сервер" in message.text) and adm[4]:
            await message.answer("📛<b>Введите название сервера.</b>")
            await st.add_server_p1.set()

        #Пользовательские обработки
        if "Профиль" in message.text:
            username=message.from_user.username
            balance =  await db.get_user_info(message.from_user.id)
            admin = str(balance[5]).replace("0", "Не забанен").replace("1", "Забанен")
            bot_username = await bot.get_me()
            ref_link=f"https://t.me/{bot_username.username}?start={message.chat.id}"
            text=f"🚩Профиль\n➖➖➖➖➖➖➖➖➖➖\n👤Имя пользователя: {username}\n💸Баланс: {misc.beauty_int(balance[1])} RUB\nСтатус: {admin}\n🔗Реферальная ссылка:\n{ref_link}"
            await message.answer(text, reply_markup=kb.profile_markup())
        elif "Правила проекта" in message.text:
            await message.answer("<b>❗ Правила</b>\n\n1️⃣.Поддержка\n  <i><b>№1.1</b>-Каждому покупателю, в случае возникновения проблемы с товаром, либо возникновения неполадки по другим причинам обязана выдаться поддержка. </i>\n  <i><b>№1.2</b>-При нарушении правил, поддержка имеет право на отказ о предоставлении помощи (см. правило №1.1)</i>\n  <i><b>№1.3</b>-В случае плохого отношения к агентам тех.поддержки, поддержка имеет право на отказ о предоставлении помощи (см. правило №1.1)</i>\n\n2️⃣.Запреты\n<b>При нарушении данного свода правил, мы имеем право на изьятие приобретенного товара, без возвращения финансов.</b>\n  <i><b>№2.1</b>-Запрещается использование открытых дыр ради получения собственной выгоды.</i>\n  <i><b>№2.2</b>-Запрещено умышленное добавление ip наших серверов в чс различных проектов.</i>\n  <i><b>№2.3</b>-Запрещены DDOS-атаки с использованием наших ip адресов.</i>\n  <i><b>№2.4</b>-Запрещено использовать VPN сервера нашего магазина для анонимизации своей личности ради скрытия незаконных действий на территории стран СНГ.</i>\n\n3️⃣.Товар\n  <i><b>№3.1</b>-Получение товара происходит автоматически.</i>\n  <i><b>№3.2</b>-При выдаче невалидного товара поддержка имеет обязательство выдать вам рабочий товар на замену, либо вернуть вам потраченную сумму на покупку товара.</i>\n\n4️⃣.Поощрения\n  <i><b>№4.1</b>-За любое выявление уязвимости в магазине пользователь обязан получить вознаграждение.</i>")
        elif "Поддержка" in message.text:
            await message.answer("<b>✍ Напишите свой вопрос для отправки в тех.поддержку</b>")
            await st.help_user.set()
        elif "Купить конфиг" in message.text:
            data_for_kb = []
            servers = await db.get_servers()
            for i in servers:
                data_for_kb.append([i[1], i[0]])
            await message.answer("🗺 <b>Выберите локацию</b>", reply_markup=kb.loc_choice_markup(data_for_kb))
    else:
        await message.answer("<b>Ты забанен и не можешь использовать функции этого бота.</b>")

@dp.message_handler(state=st.change_bal, content_types=["text"])
async def change_bal(message: types.Message, state: FSMContext):
    balance = message.text
    data = await state.get_data()
    user = data.get("case")
    await db.write_balance(int(balance), user)
    await message.answer(f"✅Успешно, баланс пользователя <b>{user}</b> изменен на <b>{balance}</b>.")
    await state.finish()

@dp.message_handler(state=st.add_server_p1, content_types=["text"])
async def add_server_p1(message: types.Message, state: FSMContext):
    text = message.text
    await state.finish()
    await message.answer("📊<b>Введи данные сервера в формате</b>\n<i>Ip:Имя пользователя:Пароль</i>")
    await st.add_server_p2.set()
    await state.update_data(name=text)

@dp.message_handler(state=st.add_server_p2, content_types=["text"])
async def add_server_p1(message: types.Message, state: FSMContext):
    server_data = message.text.split(":")
    data = await state.get_data()
    name = data.get("name")
    await state.finish()
    ip = server_data[0]
    username = server_data[1]
    paswd = server_data[2]
    await db.add_server(name, ip, username, paswd)
    await message.answer(f"✅Успешно, сервер <b>{name}</b> добавлен.")

#Обработчик изменения настроек
@dp.message_handler(state=st.settings, content_types=["text"])
async def settings(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    cas = data.get("case")
    await state.finish()
    match cas:
        case "price":
            await db.set_price(int(text))
            await message.answer(f"✅Успешно, новая цена за конфиг: <b>{text}</b>")

#Обработчик активации промокода
@dp.message_handler(state=st.act_promo, content_types=["text"])
async def promo(message: types.Message, state: FSMContext):
    promo=message.text
    promoinf = await db.get_promo_info(promo)
    if promoinf:
        if promoinf[3] > 0:
            user_info = await db.get_user_info(message.from_user.id)
            if user_info[2] != None: early_activated = user_info[2]
            else: early_activated = ""
            act_promos = early_activated.split("|")
            if promo not in act_promos:
                userbalance = user_info[1]
                new_user_balance = userbalance + promoinf[2]
                act_count=promoinf[3]
                act_count-=1
                pr=f"{early_activated}{promo}|"
                await db.write_balance(new_user_balance, message.from_user.id)
                await db.write_act_count(act_count,promo)
                await db.write_act_promos(pr, message.from_user.id)
                await message.answer(f"✅Успешно, ваш промокод найден и активирован.\n💰Ваш баланс: <b>{misc.beauty_int(new_user_balance)}</b>")
            else:
                await message.answer("❌Вы уже активировали данный промокод.")
        else:
            await message.answer("❌Колличество активаций данного промокода закончилось.")
    else:
        await message.answer("❌Промокод не найден.")
    await state.finish()

#Обработчик пополнения баланса
@dp.message_handler(state=st.add_funds, content_types=["text"])
async def add_funds(message: types.Message, state: FSMContext):
    summ = message.text
    await message.answer("🤔 <b>Выберите сервис</b>", reply_markup=kb.payment_service_markup(summ, "0"))
    await state.finish()

#Обработчик добавления промокода ЧАСТЬ 1
@dp.message_handler(state=st.add_promo_p1, content_types=["text"])
async def promo_p1(message: types.Message, state: FSMContext):
    promo = message.text
    await state.finish()
    await message.answer("💸 <b>Введите сумму промокода:</b>")
    await st.add_promo_p2.set()
    await state.update_data(promo=promo)

#Обработчик добавления промокода ЧАСТЬ 2
@dp.message_handler(state=st.add_promo_p2, content_types=["text"])
async def promo_p2(message: types.Message, state: FSMContext):
    try:
        summ = int(message.text)
    except ValueError:
        await message.answer("☹ <b>Ты ввел не число, ввод отменен.</b>")
        await state.finish()
    else:
        data = await state.get_data()
        promo=data.get("promo")
        await state.finish()
        await message.answer("♾ <b>Введите колличество активаций промокода.</b>")
        await st.add_promo_p3.set()
        await state.update_data(promo=promo, summ=summ)

#Обработчик добавления промокода ЧАСТЬ 3
@dp.message_handler(state=st.add_promo_p3, content_types=["text"])
async def promo_p2(message: types.Message, state: FSMContext):
    try:
        act_count = int(message.text)
    except ValueError:
        await message.answer("☹ <b>Ты ввел не число, ввод отменен.</b>")
        await state.finish()
    else:
        data = await state.get_data()
        promo=data.get("promo")
        summ=data.get("summ")
        await state.finish()
        await db.create_promo(promo, summ, act_count)
        await message.answer("✅<b>Успешно</b>")

#Обработчик тех-поддержки СТОРОНА ЮЗЕРА
@dp.message_handler(state=st.help_user, content_types=["text"])
async def to_admin(message: types.Message, state: FSMContext):
    text = f"❔ <b>Поступил новый запрос:</b>\n<b>От: </b>{message.from_user.mention}\n<b>🆔ID: {message.from_user.id}</b>\n\n{message.text}"
    await bot.send_message(config.group_id, text, reply_markup=kb.help_markup(message.from_user.id))
    await message.answer(f"<b>✅ Ваш вопрос был успешно отправлен тех.поддержке!</b>")
    await state.finish()

#Обработчик тех-поддержки СТОРОНА АДМИНА
@dp.message_handler(state=st.help_admin, content_types=["text"])
async def to_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    admin_id=data.get("padmin")
    if message.from_user.id == admin_id:
        text=f"🥳 <b>Тех.поддержка ответила на ваш вопрос:</b>\n\n {message.text}"
        id = data.get("uid")
        await bot.send_message(id, text)
        await message.answer("✅ <b>Ответ был отправлен пользователю!</b>")
        await state.finish()

#Обработчик рассылки
@dp.message_handler(state=st.mailing, content_types=["text"])
async def mailing(message: types.Message, state:FSMContext):
    text=message.text
    if "Обратно" not in text:
        await state.finish()
        await message.answer("Начинаю рассылку", reply_markup=kb.admin_keyboard())##
        users = await db.all_userids()
        sended=0
        non_sended=0
        for i in users:
            try: await bot.send_message(i[0], text)
            except: non_sended+=1
            else: sended+=1
        await message.answer(f"📍 <b>Рассылка закончена!</b>\n\n🟢 Отправлено: {sended}\n🔴 Не отправлено: {non_sended}")
    else:
        await message.answer("👑Админ панель", reply_markup=kb.admin_keyboard())

#Обработчик выдачи админки
@dp.message_handler(state=st.new_admin_id_input, content_types=["text"])
async def new_admin(message: types.Message, state: FSMContext):
    id=message.text
    user_info = await db.get_user_info(id)
    if user_info:
        if not user_info[4]:
            await message.answer("👌<b> Ок</b>")
            await db.set_admin(id, 1)
        else:
            await message.answer("<b>✅ Этот пользователь уже админ</b>")
    else:
        await message.answer("<b>🤔 Такого айди нет в базе данных</b>")
    await state.finish()

#Обработчик снятия админки
@dp.message_handler(state=st.cancell_admin, content_types=["text"])
async def cancell_admin(message: types.Message, state: FSMContext):
    id=message.text
    user_info = await db.get_user_info(id)
    if user_info:
        if user_info[4]:
            await message.answer("👌<b> Ок</b>")
            await db.set_admin(id, 0)
        else:
            await message.answer("<b>✅ Этот пользователь уже админ</b>")
    else:
        await message.answer("<b>🤔 Такого айди нет в базе данных</b>")
    await state.finish()

#Обработчик информации о юзере
@dp.message_handler(state=st.users_control_input, content_types=["text"])
async def users_control(message: types.Message, state: FSMContext):
    userid=message.text
    adm = await db.get_user_info(message.chat.id)
    if "Обратно" not in userid:
        user_info = await db.get_user_info(userid)
        if user_info != None:
            activated_pormos = str(user_info[2]).replace("None", "Нет")
            inviter = str(user_info[3]).replace("None", "Нет")
            blocked = str(user_info[5]).replace("0", "Не заблокирован").replace("1", "Заблокирован")
            admin = str(user_info[4]).replace("0", "Нет").replace("1", "Да")
            await message.answer(f"👁️‍🗨️ <b>Информация о пользователе</b>\n\n🆔 <b>ID:</b>{user_info[0]}\n💰 <b>Баланс:</b>{misc.beauty_int(user_info[1])}\n🏷 <b>Активированные промокоды: </b>{activated_pormos}\n👻 <b>Пригласивший: </b>{inviter}\n🧐 <b>Статус: </b>{blocked}\n😎 <b>Админ: </b>{admin}", reply_markup=kb.change_user_balance_markup(userid))
        else:
            await message.answer("❌Нету такого пользователя.", reply_markup=kb.admin_keyboard())
    else:
        if adm[4]:
            await message.answer(f'🤝Добро пожаловать <b>{message.from_user.username}</b>', reply_markup=kb.main_admin_markup())
        else:
            await message.answer(f'🤝Добро пожаловать <b>{message.from_user.username}</b>', reply_markup=kb.main_user_markup())
    await state.finish()

#Ifmain Запуск пулинга
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
