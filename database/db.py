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

def auth(login, password):
    with connect:
        cursor.execute(f'SELECT * FROM `user` WHERE `login`="{login}" AND `password`="{password}"')
        result = cursor.fetchall()
        if len(result)!=0:
            return result
        else:
            return "Неверный логин или пароль"

def reg(login, password):
    with connect:
        cursor.execute(f'SELECT `login` FROM `user` WHERE `login`="{login}"')
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
            else:
                print("Дошёл")
                cursor.execute(f"INSERT INTO `user`(`login`, `password`, `is_admin`) VALUES ('{login}','{password}', {False})")
                connect.commit()
                return "Вы успешно зарегестрировались"

def catalog():
    with connect:
        cursor.execute(f'SELECT * FROM `item`')
        result = cursor.fetchall()
        return result

def feedback(id_user):
    with connect:
        cursor.execute(f'SELECT * FROM `feedback` WHERE `id_user` = "{id_user}"')
        result = cursor.fetchall()
        return result