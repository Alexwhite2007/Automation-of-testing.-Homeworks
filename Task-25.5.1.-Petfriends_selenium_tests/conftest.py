import pytest as pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings import email, password


@pytest.fixture(autouse=True)
def driver_fixture():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    # Используем здесь неявное ожидание
    pytest.driver.implicitly_wait(7)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


@pytest.fixture()
def login_and_go_to_my_pets():
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'email'))).send_keys(email)
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'pass'))).send_keys(password)
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы'))).click()

    assert WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h2'))).text == "apitestmail@mail.com"
