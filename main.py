import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920x1080")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10, 1)

driver.get(url="https://www.tinkoff.ru/bank/help/interfaces/online-banking/start/enter/")
try:
    NEXT_BUTTON = ('xpath', '//span[@data-qa-type="uikit/button.content"]')
    wait.until(EC.visibility_of_element_located(NEXT_BUTTON))
    driver.find_element(*NEXT_BUTTON).click()
    driver.switch_to.window(driver.window_handles[1])
except BaseException:
    print('Ошибка перехода в окно для ввода номера')

try:
    NUMBER_PHONE = ('xpath', '//input')
    wait.until(EC.visibility_of_element_located(NUMBER_PHONE))
    phone = input('Введите номер телефона: +7')
    wait.until(EC.visibility_of_element_located(NUMBER_PHONE))
    driver.find_element(*NUMBER_PHONE).send_keys(phone)
    driver.find_element(*NUMBER_PHONE).send_keys(Keys.ENTER)
except BaseException:
    print('Ошибка в блоке ввода номера')

try:
    sms = input('Введите код из смс: ')
    SMS_CODE = ('xpath', '//input')
    wait.until(EC.visibility_of_element_located(SMS_CODE))
    driver.find_element(*SMS_CODE).send_keys(sms)
except BaseException:
    print('Ошибка в блоке вввода смс')

try:
    PASSWORD = ('xpath', '//input[@name="password"]')
    password = input('Введите пароль: ')
    wait.until(EC.visibility_of_element_located(PASSWORD))
    driver.find_element(*PASSWORD).send_keys(password)
    driver.find_element(*PASSWORD).send_keys(Keys.ENTER)
except BaseException:
    print('Ошибка в блоке ввода пароля')

file_name = input('Введите название файла (убедитесь, что файла с таким названием не существует): ')
file_name += '.txt'

try:
    NOT_NOW_BUTTON = ('xpath', '//button')
    wait.until(EC.visibility_of_element_located(NOT_NOW_BUTTON))
    wait.until(EC.element_to_be_clickable(NOT_NOW_BUTTON))
    driver.find_element(*NOT_NOW_BUTTON).click()
except BaseException:
    print('Ошибка в блоке отказа для создания кода быстрой авторизации')

try:
    ALL = ('xpath', '//a[@data-schema-path="title"]')
    wait.until(EC.element_to_be_clickable(ALL))
    driver.find_element(*ALL).click()
except:
    print('Ошибка при переходе на новую вкладку')

try:
    ALL_CATEGORY = ('xpath', '//div[@data-appearance="elevated"]//div/div/div/ul/li/div/a')
    wait.until(EC.element_to_be_clickable(ALL_CATEGORY))
    categoryes = driver.find_elements(*ALL_CATEGORY)
    links = [category.get_attribute('href') for category in categoryes]
    links = links[3::]
except BaseException:
    print('Ошибка в последнем блоке')

result = []
try:
    marker = ('xpath', '//div[@data-schema-path="offer"]')
    for link in links:
        print('В процессе...')
        driver.get(link)
        wait.until(EC.element_to_be_clickable(marker))
        wait.until(EC.visibility_of_element_located(marker))
        title = driver.find_element('xpath', '//h1').text

        # скролим страницу
        start_time = time.time()
        while True:
            driver.execute_script('scrollBy(0,350)')
            if time.time() - start_time > 4:
                break

        all_cashback = driver.find_elements(*marker)
        for cashback in all_cashback:
            result.append(cashback.text)
        with open(file_name, mode='a', encoding='utf-8') as file:
            file.write(title)
            file.write('\n')
            for group in result:
                lst_of_group = group.split('\n')
                str_of_group = ' '.join(lst_of_group)
                file.write(str_of_group)
                file.write('\n')

        result.clear()

    print('Готово')

except BaseException:
    print('Ошибка при сборе данных по ссылке')
