from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_dropdown_select_and_change():
    
    # Abrimos el navegador 
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Primero abrimos la URL
        driver.get("https://the-internet.herokuapp.com/dropdown")

        # Esperamos a que el dropdown aparezca
        dropdown_element = wait.until(
            EC.presence_of_element_located((By.ID, "dropdown"))
        )

        dropdown = Select(dropdown_element)

        # Comprobamos que por defecto está la opción "Please select an option"
        default_text = dropdown.first_selected_option.text
        assert default_text == "Please select an option"

        # Seleccionamos Option 1
        dropdown.select_by_visible_text("Option 1")
        selected_text = dropdown.first_selected_option.text
        assert selected_text == "Option 1"

        # Seleccionamos Option 2
        dropdown.select_by_visible_text("Option 2")
        selected_text = dropdown.first_selected_option.text
        assert selected_text == "Option 2"

        # Volver a seleccionar Option 2 (no cambia)
        dropdown.select_by_visible_text("Option 2")
        selected_text = dropdown.first_selected_option.text
        assert selected_text == "Option 2"

        # Recargar la página y validar reset
        driver.refresh()
        dropdown_element = wait.until(
            EC.presence_of_element_located((By.ID, "dropdown"))
        )
        dropdown = Select(dropdown_element)
        default_text = dropdown.first_selected_option.text
        assert default_text == "Please select an option"

    finally:
        driver.quit()
