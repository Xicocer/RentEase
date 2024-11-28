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

def reg(name, password_confirm,password ,email):
    with connect:
        cursor.execute(f'SELECT id, email FROM user WHERE email="{email}"')
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
            elif password == password_confirm :
                return "Пароли отличаются"
            else:
                cursor.execute(f"INSERT INTO user(email, password, name) VALUES ('{email}','{password}', {name})")
                connect.commit()
                return "Вы успешно зарегистрировались"
def auth(email, password):
    with connect:
        cursor.execute(f'SELECT * FROM user WHERE email="{email}" AND password = "{password}"')
        result = cursor.fetchall()
    if len(result)==0:
        return "Данные введены не верно"
    else :
        return result
def get_feadbacks(id_item):
    with connect:
        cursor.execute(f"SELECT * FROM feedback WHERE active = 1 AND id_item = {id_item}")
        result = cursor.fetchall()
        return result
