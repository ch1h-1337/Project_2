from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unittest


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        # Указываем путь к webdriver (например, Chrome)
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        driver = self.driver
        driver.get("http://localhost:5000/")  # Главная страница

        # Проверяем, что на главной странице есть какое-то ключевое слово
        self.assertIn("Домашняя страница", driver.title)  # Это можно заменить на слово, которое ожидается на главной странице

    def test_about_page(self):
        driver = self.driver
        driver.get("http://localhost:5000/about")  # Страница "О нас"

        # Проверяем, что на странице "О нас" есть какое-то ключевое слово
        self.assertIn("О нас", driver.title)  # Опять же, это можно заменить на что-то, что точно есть на странице

    def test_login_page_loads(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")  # Страница входа

        # Проверяем, что заголовок страницы содержит слово "Вход"
        self.assertIn("Вход", driver.title)

    def test_login_with_invalid_credentials(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        # Заполняем форму неверными данными
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("wrong_username")
        password_input.send_keys("wrong_password")

        # Отправляем форму
        password_input.send_keys(Keys.RETURN)

        # Явное ожидание появления ошибки
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))

        # Проверяем, что блок с ошибкой появился и содержит текст ошибки
        error_message = driver.find_element(By.CLASS_NAME, "alert-danger")
        self.assertTrue(error_message.is_displayed())
        self.assertIn("Неверное имя пользователя или пароль", error_message.text)

    def test_login_with_valid_credentials(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        # Заполняем форму правильными данными
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("admin")  # Используйте реальные учетные данные
        password_input.send_keys("password")

        # Отправляем форму
        password_input.send_keys(Keys.RETURN)

        try:
            # Явное ожидание появления элемента на главной странице
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Добро пожаловать')]"))
            )
            # Проверяем, что на главной странице появилось приветствие
            welcome_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Добро пожаловать')]")
            self.assertTrue(welcome_message.is_displayed())
        except TimeoutException:
            print("Элемент не найден в течение 10 секунд!")


if __name__ == "__main__":
    unittest.main()
