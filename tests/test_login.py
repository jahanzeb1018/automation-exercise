from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://the-internet.herokuapp.com/login"

def open_login(driver):
    driver.get(BASE_URL)

def get_flash_message(driver):
    return driver.find_element(By.ID, "flash").text

def test_login_success():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        open_login(driver)

        # Esperamos a que los inputs aparezcan
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # Uso de credenciales correctas
        username.send_keys("tomsmith")
        password.send_keys("SuperSecretPassword!")
        login_btn.click()

        # Validar banner verde. Verificamos que se realiza el login correctamente
        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        assert "You logged into a secure area!" in flash

        # Verificamos que se realiza el Logout al hacer click en él
        logout_btn = driver.find_element(By.CSS_SELECTOR, "a.button")
        logout_btn.click()

        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        assert "You logged out of the secure area!" in flash

    finally:
        driver.quit()


def test_login_wrong_user_correct_pass():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        open_login(driver)

        # Esperamos a que los inputs aparezcan
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # Comprobación con usuario erroneo y password correcto
        username.send_keys("hola")
        password.send_keys("SuperSecretPassword!")
        login_btn.click()

        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid!" in flash

        # Validamos que los campos quedan vacíos
        assert driver.find_element(By.ID, "username").get_attribute("value") == ""
        assert driver.find_element(By.ID, "password").get_attribute("value") == ""

    finally:
        driver.quit()


def test_login_correct_user_wrong_pass():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        open_login(driver)

        # Esperamos a que los inputs aparezcan
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # Comprobación con usuario correcto y password erroneo
        username.send_keys("tomsmith")
        password.send_keys("hola123")
        login_btn.click()

        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        assert "Your password is invalid!" in flash

        assert driver.find_element(By.ID, "username").get_attribute("value") == ""
        assert driver.find_element(By.ID, "password").get_attribute("value") == ""

    finally:
        driver.quit()


def test_login_empty_fields():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        open_login(driver)

        # Esperamos a que el boton del login cargue y comprobamos con los inputs vacios
        login_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_btn.click()

        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid!" in flash

    finally:
        driver.quit()


def test_login_user_empty_pass_correct_and_user_correct_pass_empty():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Caso A: user correcto, pass vacía siguiendo la misma logica que los tests anteriores
        open_login(driver)

        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        username.send_keys("tomsmith")
        login_btn.click()

        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        assert "Your password is invalid!" in flash

        # Caso B: user vacío, pass correcta siguiendo la misma logica que los tests anteriores
        open_login(driver)

        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        password.send_keys("SuperSecretPassword!")
        login_btn.click()

        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid!" in flash

    finally:
        driver.quit()
