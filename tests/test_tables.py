from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_tables_sort_due_desc_and_check_row2():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/tables")

        # Esperar a que la tabla Example 1 exista
        table = wait.until(
            EC.presence_of_element_located((By.ID, "table1"))
        )

        # Esperamos a que la cabecera "Due" exista
        due_header = table.find_element(
            By.XPATH, ".//th[@class='header']/span[normalize-space()='Due']/parent::th"
        )

        # Click 2 veces para ordenar descendente la columna "Due". Primer click ascendente y segundo descendente
        due_header.click()

        # Esperamos a que tras el primer click el orden sea ASC (primer Due = $50.00)
        wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, "#table1 tbody tr:nth-child(1) td:nth-child(4)").text == "$50.00"
        )

        due_header.click()

        # Esperamos a que tras el segundo click el orden sea DESC (primer Due = $100.00)
        wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, "#table1 tbody tr:nth-child(1) td:nth-child(4)").text == "$100.00"
        )

        # Esperamos a que haya filas
        rows = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#table1 tbody tr"))
        )
        assert len(rows) == 4


        # Obtenemos todos los valores Due del estado actual de la tabla 
        dues_text = [
            row.find_elements(By.TAG_NAME, "td")[3].text
            for row in rows
        ]

        # Covertimos el formato de los numeros
        dues_numeric = [
            float(value.replace("$", "")) for value in dues_text        
        ]

        # Creamos una lista ordenada descendente para luego comparar
        expected_desc = sorted(dues_numeric, reverse=True)

        # Validamos que la lista de la tabla es DESCENDENTE. En caso contrario mostramos error
        assert dues_numeric == expected_desc, \
            f"Los valores de Due no están en descendente. Actual: {dues_numeric}, Esperado: {expected_desc}"

        # Comprobamos el valor de la Fila 2
        row2 = rows[1]

        # Comprobamos de la fila 2 el valor para la columna Due 
        due_value_row2 = row2.find_elements(By.TAG_NAME, "td")[3].text

        # Validamos que el Due de la fila 2 es $51
        assert due_value_row2 == "$51.00"

    finally:
        driver.quit()
