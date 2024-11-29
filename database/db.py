import pymysql

try:
    connect = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='root',
                            password='',
                            database='rentease1',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = connect.cursor()
except Exception as ex:
    print(ex)

def reg(name, email, password, password_confirm):
    cursor.execute(f'SELECT `email` FROM `user` WHERE `email` = "{email}"')
    result = cursor.fetchall()
    if len(result)!=0:
        return "Такой логин уже существует"

    else:
        if len(password) < 8:
            return "Ваш пароль менее 8 символов"
        elif not any(map(str.isdigit, password)):
            return "Убедитесь, что в вашем пароле есть цифра"
        elif not any(map(str.isupper, password)):
            return "Убедитесь, что в вашем пароле есть заглавная буква"
        elif password != password_confirm :
            return "Пароли отличаются"
        elif "@" not in email:
            return "Почта должна содержать символ '@'"
        elif "mail" not in email:
            return "Почта должна содержать 'mail'"
        else:
            cursor.execute(f"INSERT INTO `user`(`is_admin`, `email`, `password`, `name`) VALUES ('{False}', '{email}','{password}', '{name}')")
            connect.commit()
            return "Вы успешно зарегистрировались"

def auth(email, password):
    cursor.execute(f'SELECT * FROM `user` WHERE `email`="{email}" AND `password` = "{password}"')
    result = cursor.fetchall()
    if len(result)==0:
        return "Данные введены неверно"
    else:
        return result

def get_feadbacks(id_item):
    cursor.execute(f"SELECT * FROM `feedback` WHERE `active` = 1 AND `id_item` = '{id_item}'")
    result = cursor.fetchall()
    return result


def get_items():
    cursor.execute(f"SELECT * FROM `items` ORDER BY `id` DESC")
    result = cursor.fetchall()
    return result

def get_categories():
    cursor.execute(f"SELECT * FROM `category` ORDER BY `id` DESC")
    result = cursor.fetchall()
    return result


def get_search(title):
    cursor.execute(f"SELECT * FROM `items` WHERE `title` LIKE '%{title}%'")
    result = cursor.fetchall()
    if len(result) != 0:
        return result
    else:
        return "Такого товара нет"
