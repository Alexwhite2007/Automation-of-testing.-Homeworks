from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

# инициализируем созданную библиотеку, присваиваем её значение переменной pf
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем возможность получения ключа с валидными данными пользователя (email, password).
     Запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # отправляем запрос на получение ключа, возвращается статус и результат:
    status, result = pf.get_api_key(email, password)
    # сравниваем полученные статус и результат с ожидаемыми значениями
    assert status == 200
    assert 'key' in result
    # print(result['key'])   # можно посмотреть данные ключа


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем api ключ и сохраняем в переменную auth_key.
       Далее, используя этот ключ, запрашиваем список всех питомцев и проверяем что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо ''"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key. При запросе возвращается статус и результат,
    # в данном случае статус нам не нужен, поэтому ставим нижнее подчеркивание _
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос на получение списка питомцев, возвращается статус и результат:
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сравниваем полученные статус и результат с ожидаемыми значениями
    assert status == 200
    assert len(result['pets']) > 0
    # print(len(result['pets']))  # можно посмотреть количество питомцев в списке,
    # но в данный момент больше 100 не показывает


def test_add_new_pet_with_valid_data(name='Вениамин', animal_type='мальтезе', age='5',
                                     pet_photo='images/veniamin.jpg'):
    """Проверяем возможность добавить карточку питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и получаем в ответ статус запроса и результат
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] is not None
    # print(result['name'])   # можно посмотреть имя добавленного питомца из результата


def test_successful_update_self_pet_info(name='Веня', animal_type='мальтийская болонка', age=4):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев. При запросе возвращается статус и результат,
    # в данном случае статус нам не нужен, поэтому ставим нижнее подчеркивание _
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то получаем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и список своих питомцев. При запросе возвращается статус и результат,
    # в данном случае статус нам не нужен, поэтому ставим нижнее подчеркивание _
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев. Значение статуса не важно, ставим _
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


    # ТЕСТ 1 (Добавление нового питомца без фото)

def test_add_new_pet_simple_without_photo(name='Балбес', animal_type='собака', age='3'):
    """Проверяем возможность добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и получаем в ответ статус запроса и результат
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    # print(result['name'])  # можно посмотреть имя добавленного питомца в результате


    # ТЕСТ 2 (Добавление фото в карточку питомца)

def test_add_photo_of_pet(pet_photo='images/dog.jpg'):
    """Проверяем возможность добавить фото в карточку существующего питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца без фото и запрашиваем список своих питомцев
    pf.add_new_pet_simple_without_photo(auth_key, "Балбес", "собака", "3")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] is not None   # проверка, что фото есть
    # print(result['pet_photo'])  # можно посмотреть данные добавленной фотографии


    # ТЕСТ 3 (Проверка на ввод невалидных данных логина и пароля, статус = 403)

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяем возможность получить api ключ с невалидными данными пользователя.
    Запрос api ключа возвращает статус 403 и в результате не содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403   # Означает что передана неверная комбинация email-password
    assert 'key' not in result


    # ТЕСТ 4 (Проверка на ввод валидного логина и невалидного пароля, статус = 403)

def test_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем возможность получить api ключ с невалидным паролем.
    Запрос api ключа возвращает статус 403 и в результате не содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403   # Означает что передана неверная комбинация email-password
    assert 'key' not in result


    # ТЕСТ 5  (Проверка на ввод невалидного логина и валидного пароля, статус = 403)

def test_api_key_with_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем возможность получить api ключ с невалидным email.
    Запрос api ключа возвращает статус 403 и в результате не содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403   # Означает что передана неверная комбинация email-password
    assert 'key' not in result


    # ТЕСТ 6  (Проверка возможности добавки питомца без данных, кроме фотографии. БАГ)

def test_add_new_pet_with_empty_data(name='', animal_type='', age='', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавить карточку питомца с одной фотографией, но без остальных данных"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца с пустыми данными и фото
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200    # Код 200 означает, что введенные невалидные данные система приняла, это ошибка.
    assert result['name'] == ''  # проверяем что в результате имя имеет пустое значение
    """ Добавляется карточка питомца только с фотографией, без остальных данных, это БАГ"""


    # ТЕСТ 7 (Проверка возможности добавки питомца с некорректными данными возраста 100 лет. БАГ)

def test_add_pet_with_incorrect_age(name='Прыгнарук', animal_type='Кот', age='100',
                                    pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавить карточку питомца с некорректным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца, от сервера возвращается статус запроса и результат
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # сверяем полученный от сервера статус и результат с ожидаемыми значениями
    # assert status == 200    # Код 200 означает, что введенные невалидные данные система приняла, это ошибка.
    assert result['age'] == '100'  # сверяем, что возраст принял некорректное указанное значение
    """ Добавляется карточка питомца c некорректным возрастом, это БАГ"""


    # ТЕСТ 8 (Проверка возможности добавки питомца с некорректными данными - спецсимволы. БАГ)

def test_add_pet_with_invalid_symbols(name='%@!*', animal_type='&^%', age='***'):
    """Проверяем возможность добавить карточку питомца с некорректными данными (спецсимволы)"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200  # Код 200 означает, что введенные невалидные данные система приняла, это ошибка.
    # Сверяем, что добавленный питомец содержит введенные некорректные данные в имени
    assert result['name'] == '%@!*'
    """ Добавляется карточка питомца c некорректными данными (спецсимволы), это БАГ"""


    # ТЕСТ 9 (Проверка возможности удаления питомца с невалидным auth_key)

def test_delete_pet_by_invalid_auth_key():
    """Проверяем возможность удалить карточку питомца с невалидным значением auth_key"""

    # Получаем ключ auth_key и список своих питомцев. При запросе возвращается статус и результат,
    # в данном случае статус нам не нужен, поэтому ставим нижнее подчеркивание _
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление c невалидным auth_key
    pet_id = my_pets['pets'][0]['id']
    invalid_auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729"}
    status, _ = pf.delete_pet(invalid_auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев. Значение статуса не важно, ставим _
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 403  # код 403 означает, что указанный ключ не валидный


    # ТЕСТ 10 (Проверка возможности изменения в карточке питомца данных, на невалидные. БАГ).

def test_update_pet_with_invalid_data(animal_type='صسغذئآ', age=-100):
    """Проверяем возможность изменения данных питомца, меняем на следующие значения:
    # Значение 'name' - строка 255 символов: буквы (прописные и строчные, лат. и кир.) и цифры,
    # Значение 'animal_type' - Группа символов из арабского письма,
    # Значение 'age' - имеет отрицательное значение. _______БАГ """

    file = open('255symbols.txt', 'r')   # открываем файл на чтение
    name = file.read()  # присваиваем содержимое файла (255 символов) переменной name
    print(name)  # можно посмотреть значение name
    file.close()  # закрываем файл

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем что статус ответа = 200, это означает что данные были изменены, это ошибка.
        assert status == 200
        assert result['name'] == name
        print(my_pets['pets'][0]['name'])   # смотрим текущее значение name
        print(my_pets['pets'][0]['animal_type'])  # смотрим текущее значение animal_type
    else:
        # если список питомцев пустой, то получаем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")
    """ Карточка питомца обновляется некорректными данными, это БАГ"""
