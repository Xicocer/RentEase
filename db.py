import psycopg2
import emoji
from aiogram.filters.state import StatesGroup, State

conn = psycopg2.connect(user="postgres",
                        password="root",
                        host="localhost",
                        port="5432",
                        database="chatbot")

with conn:
    curser = conn.cursor()


    class Person(StatesGroup):
        """
        Класс для хранения данных пользователя во время регистрации
        """
        full_name = State()
        age = State()
        time = State()
        day = State()
        gender = State()
        id_tg = State()
        update = State()
        id_advice = State()
        edit_advice = State()


    async def add_user(data):
        """
        Метод регистрации пользователя. Заносит данные пользователя в БД
        :param: данные о пользователе
        """
        id = curser.execute("""SELECT MAX(id) AS id FROM public."user" """)
        id = curser.fetchone()
        if id[0] is None:
            id = 0
        else:
            id = int(id[0])
        id += 1
        curser.execute("""INSERT INTO public."user"(
            id, full_name, age, gender, id_tg)
            VALUES (%s, %s, %s, %s, %s);""", (id, data['full_name'], data['age'], data["gender"], data["id_tg"], False))
        if data["day"] == "Рабочие дни":
            for i in range(5):
                curser.execute("""INSERT INTO public."user_time"(
                    user_id, day, "time")
                    VALUES (%s, %s, %s);""", (id, i+1, data["time"]))
        elif data["day"] == "Выходные дни":
            curser.execute("""INSERT INTO public."user_time"(
                user_id, day, "time")
                VALUES (%s, %s, %s);""", (id, 0, data["time"]))
        conn.commit()
        return 'Данные успешно добавлены'


    async def update_user(data):
        """
        Метод для обновления данных о пользователе
        :param: данные о пользователе
        """
        id = curser.execute(f"""SELECT * FROM public."user" WHERE id_tg = {int(data["id_tg"])} """)
        id = curser.fetchone()
        curser.execute("""UPDATE public."user" SET full_name = %s, age = %s, gender = %s WHERE id_tg = %s""",
                       (data["full_name"], data["age"], data["gender"], data["id_tg"]))
        if data["day"] == "Рабочие дни":
            for i in range(5):
                curser.execute("""UPDATE public."user_time" SET day = %s, time = %s WHERE user_id = %s;""",
                               (i+1, data["time"], id[0]))
        elif data["day"] == "Выходные дни":
            curser.execute("""UPDATE public."user_time" SET day = %s, time = %s WHERE user_id = %s;""",
                           (0, data["time"], id[0]))
        conn.commit()


    async def advice(id_tg):
        """
        Функция выводит 1 рекомендацию, которую пользователь никак не отметил
        :param id_tg: id профиля в Telegram
        """
        id = await get_user(id_tg)
        id = id[0][0]
        lst_advice = curser.execute(f"""SELECT MAX (id_advice) FROM public."user_to_advice" WHERE id_user = {id}""")
        lst_advice = curser.fetchone()
        if lst_advice[0] is None and lst_advice != []:
            advice = curser.execute(f"""SELECT * FROM public."advice" LIMIT 1;""")
        else:
            advice = curser.execute(f"""SELECT * FROM public."advice" WHERE id = {(lst_advice[0]+1)} LIMIT 1;""")
        advice = curser.fetchall()
        if advice is not None and advice != []:
            return advice[0]
        else:
            return 'Рекомендации кончились'


    async def change_advice(id_tg, advice, complete, verify=False):
        """
        Функция для изменения статуса рекомендации
        :param id_tg: id профиля в Telegram
        :param advice: текст рекомендации для её идентификации
        :param complete: статус, который нужно установить True или False
        :param verify: проверка на изменение или установление статуса
        """
        id = await get_user(id_tg)
        id = id[0][0]
        curser.execute("""SELECT COUNT(id) as count FROM  public."user_to_advice"  WHERE id_advice = %s AND id_user = '%s';""", (advice, id))
        check = curser.fetchone()
        if int(check[0]) and verify is True:
            curser.execute(
                f""" UPDATE public."user_to_advice" SET complete = {complete} WHERE id_user = {id} AND id_advice = {advice} """)
            conn.commit()
        elif not int(check[0]) and verify is False:
            curser.execute("""INSERT INTO public."user_to_advice" (id_user, id_advice, complete) VALUES (%s, %s, %s) """, (id, advice, complete))
            conn.commit()


    async def last_advice(id_tg):
        """
        Функция, которая выводит последние 3 рекомендации
        :param id_tg: id профиля в Telegram
        """
        advices = ""
        advice_last = await advice(id_tg)
        if advice_last != "Рекомендации кончились":
            advices += f"<b>День {advice_last[0]}. Сегодня.</b> {advice_last[1]}"
            curser.execute(f"""SELECT * FROM public."advice" WHERE id = {int(advice_last[0]) - 1} LIMIT 1;""")
            advice_one = curser.fetchone()
            if advice_one is not None and advice_one != []:
                advices += f"\n<b>День {advice_one[0]}.</b> {advice_one[1]}"
                curser.execute(f"""SELECT * FROM public."advice" WHERE id = {int(advice_last[0]) - 2} LIMIT 1;""")
                advice_two = curser.fetchone()
                if advice_two is not None and advice_two != []:
                    advices += f"\n<b>День {advice_two[0]}.</b> {advice_two[1]}"
                    return advices
                else:
                    return advices
            else:
                return advices
        else:
            curser.execute("""SELECT * FROM public."advice" WHERE id >= 1;""")
            last_advice1 = curser.fetchall()
            advices += (f"День {last_advice1[2][0]}. {last_advice1[2][1]}\n"
                     f"День {last_advice1[1][0]}. {last_advice1[1][1]}\n"
                     f"День {last_advice1[0][0]}. {last_advice1[0][1]}")
            return advices


    async def get_user(id_tg):
        """
        Функция для получения данных пользователя из БД
        :param id_tg: id профиля в Telegram
        """
        curser.execute(f"""SELECT * FROM public."user" WHERE id_tg = {int(id_tg)} """)
        user = curser.fetchall()
        if user is not None and user != []:
            return user
        else:
            return False


    async def get_time(id_tg):
        """
        Функция для получения графика уведомления пользователя
        :param id_tg: id профиля в Telegram
        """
        id = await get_user(id_tg)
        id = id[0][0]
        time = curser.execute(f"""SELECT day, time FROM public."user_time" WHERE user_id = {id} """)
        time = curser.fetchone()
        return time


    async def results(id_tg):
        """
        Функция выводит результаты пользователя
        :param id_tg: id профиля в Telegram
        """
        id = await get_user(id_tg)
        id = id[0][0]
        lst_all_advice_id = []
        lst_com = []
        for i in range(1, 31):
            com = curser.execute(
                f"""SELECT complete FROM public."user_to_advice" WHERE id_user = {id} and id_advice = {i}""")
            com = curser.fetchone()
            if com is None:
                lst_com.append(None)
            else:
                lst_com.append(com[0])
            all_advice = curser.execute(f"""SELECT * FROM public."advice" WHERE id = {i}""")
            all_advice = curser.fetchall()
            lst_advice = []
            lst_all_advice_id.append(all_advice[0])
        advice_com = zip(lst_all_advice_id, lst_com)
        lst = []
        lst_emo = []
        for j in advice_com:
            if j[1] is True:
                lst_emo.append(emoji.emojize(":check_mark_button:"))
            elif j[1] is False:
                lst_emo.append(emoji.emojize(":cross_mark:"))
            else:
                lst_emo.append(emoji.emojize(":ZZZ:"))
            lst.append(j)
        lst = list(zip(lst, lst_emo))
        return lst


    async def advice_on_id(id_tg, id_advice=None):
        """
        Функция для получения последней отмеченной Рекомендации
        :param id_advice: id Рекомендации
        :param id_tg: id профиля в Telegram
        """
        id = await get_user(id_tg)
        id = id[0][0]
        advice_id = curser.execute(f"""SELECT MAX(id_advice) FROM public."user_to_advice" WHERE id_user = {id}""")
        advice_id = curser.fetchone()
        if int(id_advice) > int(advice_id[0]):
            return "Вы еще не получили эту рекомендацию"
        else:
            advice = curser.execute(f"""SELECT advice FROM public."advice" WHERE id = {id_advice}""")
            advice = curser.fetchone()
            return advice[0]


    async def get_true_advice(id_tg):
        """
        Функция для получения всех выполненных рекомендаций
        :param id_tg: id профиля в Telegram
        """
        id = await get_user(id_tg)
        id = id[0][0]
        advice = curser.execute(f"""SELECT * FROM public."user_to_advice" WHERE id_user = {id} and complete = True""")
        advice = curser.fetchall()
        return len(advice)


    async def get_false_advice(id_tg):
        """
        Функция для получения всех выполненных рекомендаций
        :param id_tg: id профиля в Telegram
        """
        id = await get_user(id_tg)
        id = id[0][0]
        advice = curser.execute(f"""SELECT * FROM public."user_to_advice" WHERE id_user = {id} and complete = False""")
        advice = curser.fetchall()
        return advice


    async def get_user_id_tg():
        """
        Функция для получения id_tg пользователя из БД
        """
        curser.execute(f"""SELECT id_tg FROM public."user" """)
        users = curser.fetchall()
        return users


    async def advice_id(id_advice):
        """
        Функция получения рекомендации по её id
        :param id_advice:
        """
        advice = curser.execute(f"""SELECT advice FROM public."advice" WHERE id = {id_advice}""")
        advice = curser.fetchone()
        return advice[0]
