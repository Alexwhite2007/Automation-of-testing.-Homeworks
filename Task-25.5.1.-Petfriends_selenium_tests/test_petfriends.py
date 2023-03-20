import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Проверка присутствия в документе всех элементов раздела "Мои питомцы", найденных с помощью указанного локатора,
# используем явные ожидания
def test_web_elements(login_and_go_to_my_pets):
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".navbar")))  # навигационная панель
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".navbar-brand")))  # заголовок
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href='/my_pets']")))  # раздел Мои питомцы
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href='/all_pets']")))  # раздел Все питомцы
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn.btn-outline-secondary")))  # Кнопка Выйти
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn.btn-outline-success")))  # Кнопка Добавить питомца
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2")))  # заголовок с информацией о пользователе
    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".table-hover")))  # Таблица питомцев пользователя


def test_my_pets_data(login_and_go_to_my_pets):
    # Параметры питомцев оформляем в качестве переменных и записываем в список
    # Устанавливаем неявное ожидание
    pytest.driver.implicitly_wait(10)
    mypets = pytest.driver.find_elements(By.TAG_NAME, 'tr')
    images = pytest.driver.find_elements(By.CSS_SELECTOR, "div#all_my_pets > table > tbody > tr > th > img")
    names = pytest.driver.find_elements(By.CSS_SELECTOR, "div#all_my_pets > table > tbody > tr > td:nth-child(2)")
    types = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-child(3)')
    ages = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-child(4)')

    # Проверка №1 - Присутствуют все питомцы, для этого:
    # Находим кол-во питомцев по статистике пользователя и проверяем, что их число соответствует кол-ву
    # питомцев в таблице
    mypets_quantity = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split(
        '\n')[1].split(': ')[1]
    pets_counted_in_table = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(mypets_quantity) == len(pets_counted_in_table)

    # Проверка №2 - У всех питомцев есть имя, возраст и порода.
    for i in range(len(names)):
        assert ages[i].text != ''
        assert names[i].text != ''
        assert types[i].text != ''

    # Проверка №3 - хотя бы у половины питомцев есть фото
    # Устанавливаем неявные ожидания(сек)
    number_of_images = 0
    half_num = float((len(mypets) - 1) / 2)

    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_of_images += 1
        else:
            number_of_images = number_of_images
    assert number_of_images >= half_num

    # Проверка №4- У всех питомцев разные имена
    unique_names = set(names)
    assert len(names) == len(unique_names)

    # Проверка №5 - В списке нет повторяющихся питомцев.
    # Устанавливаем неявные ожидания(сек)
    unq_pets = []
    for pet in mypets:
        unq_pets.append(pet.text)
    assert len(set(unq_pets)) == len(unq_pets)
