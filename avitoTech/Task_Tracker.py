import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import unittest

# Константы локаторов
TITLE_FIELD = (By.XPATH, "//input[@required and @type='text']")
DESCRIPTION_FIELD = (
By.XPATH, "//textarea[@class='MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputMultiline css-s63k3s']")
PROJECT_FIELD = (By.XPATH, "/html/body/div[2]/div[3]/div/div[3]/div/div")
FIRST_PROJECT = (By.XPATH, "(//li[@role='option'])[1]")
ASSIGNE_FIELD = (By.XPATH, "/html/body/div[2]/div[3]/div/div[6]/div/div")
FIRST_ASSIGNE = (By.XPATH, "(//li[@role='option'])[1]")
PRIORITY_FIELD = (By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div/div")
LOW_PRIORITY = (By.XPATH, "(//li[@role='option'])[1]")
CREATE_TASK_BUTTON = (By.XPATH, "//button[contains(text(), 'Создать задачу')]")
SUBMIT_BUTTON = (By.XPATH, "/html/body/div[2]/div[3]/div/div[7]/div[2]/button")
SEARCH_FIELD = (By.CSS_SELECTOR, "input[placeholder*='Поиск']")
STATUS_FILTER = (By.XPATH,
                 "(//div[@class='MuiSelect-select MuiSelect-outlined MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputSizeSmall css-uxvpzc'])[1]")
PROJECT_FILTER = (By.XPATH,
                  "(//div[@class='MuiSelect-select MuiSelect-outlined MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputSizeSmall css-uxvpzc'])[2]")
STATUS_FIELD = (By.XPATH, "/html/body/div[2]/div[3]/div/div[5]/div/div")

# Константы для опций фильтров
MEDIUM_PRIORITY = (By.XPATH, "//li[contains(text(), 'Medium')]")
SECOND_ASSIGNEE = (By.XPATH, "(//li[@role='option'])[2]")
BACKLOG_STATUS = (By.XPATH, "//li[contains(text(), 'Backlog')]")
IN_PROGRESS_STATUS = (By.XPATH, "//li[contains(text(), 'InProgress')]")
DONE_STATUS = (By.XPATH, "//li[contains(text(), 'Done')]")
ALL_STATUS = (By.XPATH, "//li[contains(text(), 'Все')]")
REDESIGN_PROJECT = (By.XPATH, "//li[contains(text(), 'Редизайн карточки товара')]")
OPTIMIZATION_PROJECT = (By.XPATH, "//li[contains(text(), 'Оптимизация производительности')]")
ALL_PROJECTS = (By.XPATH, "//li[contains(text(), 'Все')]")

# Константы для кнопок
UPDATE_BUTTON = (By.XPATH, "//button[contains(text(), 'Обновить')]")
GO_TO_BOARD_BUTTON = (By.XPATH, "//a[contains(text(), 'Перейти на доску')]")
ALL_TASKS_BUTTON = (By.XPATH, "//a[contains(text(), 'Все задачи')]")
PROJECTS_TAB = (By.XPATH, "//a[contains(text(), 'Проекты')]")
GO_TO_BOARD_BUTTON_4 = (By.XPATH, "(//a[contains(text(), 'Перейти к доске')])[4]")


class AvitoTaskTrackerTests(unittest.TestCase):

    def setUp(self):
        #Настройка перед каждым тестом
        service = Service(executable_path=r'C:\avitoTech\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.get("https://avito-tech-internship-psi.vercel.app/index.html")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        #Очистка после каждого теста
        self.driver.quit()

    # TC001: Успешное создание задачи
    def test_TC001_successful_task_creation(self):
        create_btn = self.wait.until(EC.element_to_be_clickable(CREATE_TASK_BUTTON))
        create_btn.click()

        title_field = self.wait.until(EC.element_to_be_clickable(TITLE_FIELD))
        title_field.clear()
        title_field.send_keys("Тестовая задача")

        description_field = self.wait.until(EC.element_to_be_clickable(DESCRIPTION_FIELD))
        description_field.clear()
        description_field.send_keys("Описание тестовой задачи")

        project_field = self.wait.until(EC.element_to_be_clickable(PROJECT_FIELD))
        project_field.click()
        first_project = self.wait.until(EC.element_to_be_clickable(FIRST_PROJECT))
        first_project.click()

        priority_field = self.wait.until(EC.element_to_be_clickable(PRIORITY_FIELD))
        priority_field.click()
        priority_option = self.wait.until(EC.element_to_be_clickable(LOW_PRIORITY))
        priority_option.click()

        assignee_field = self.wait.until(EC.element_to_be_clickable(ASSIGNE_FIELD))
        assignee_field.click()
        assignee_option = self.wait.until(EC.element_to_be_clickable(FIRST_ASSIGNE))
        assignee_option.click()

        create_submit_btn = self.driver.find_element(*SUBMIT_BUTTON)
        create_submit_btn.click()
        time.sleep(2)

        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.clear()
        search_field.send_keys("Тестовая задача")
        time.sleep(2)

        task_in_list = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Тестовая задача')]")))
        self.assertTrue(task_in_list.is_displayed())

    # TC002: Валидация обязательных полей
    def test_TC002_required_fields_validation(self):
        def is_button_disabled():
            try:
                button = self.driver.find_element(*SUBMIT_BUTTON)
                return "Mui-disabled" in button.get_attribute("class")
            except:
                return False

        def is_button_enabled():
            try:
                button = self.driver.find_element(*SUBMIT_BUTTON)
                return "Mui-disabled" not in button.get_attribute("class")
            except:
                return False

        actions = ActionChains(self.driver)

        # 1) Без названия
        create_btn = self.wait.until(EC.element_to_be_clickable(CREATE_TASK_BUTTON))
        create_btn.click()

        project_field = self.wait.until(EC.element_to_be_clickable(PROJECT_FIELD))
        project_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_PROJECT)).click()

        priority_field = self.wait.until(EC.element_to_be_clickable(PRIORITY_FIELD))
        priority_field.click()
        self.wait.until(EC.element_to_be_clickable(LOW_PRIORITY)).click()

        assignee_field = self.wait.until(EC.element_to_be_clickable(ASSIGNE_FIELD))
        assignee_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_ASSIGNE)).click()

        title_field = self.wait.until(EC.element_to_be_clickable(TITLE_FIELD))
        title_field.clear()

        self.assertTrue(is_button_disabled(), "Кнопка должна быть неактивна без названия")
        actions.send_keys(Keys.ESCAPE).perform()

        # 2) Без проекта
        create_btn = self.wait.until(EC.element_to_be_clickable(CREATE_TASK_BUTTON))
        create_btn.click()

        title_field = self.wait.until(EC.element_to_be_clickable(TITLE_FIELD))
        title_field.clear()
        title_field.send_keys("Задача без проекта")

        priority_field = self.wait.until(EC.element_to_be_clickable(PRIORITY_FIELD))
        priority_field.click()
        self.wait.until(EC.element_to_be_clickable(LOW_PRIORITY)).click()

        assignee_field = self.wait.until(EC.element_to_be_clickable(ASSIGNE_FIELD))
        assignee_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_ASSIGNE)).click()

        self.assertTrue(is_button_disabled(), "Кнопка должна быть неактивна без проекта")
        actions.send_keys(Keys.ESCAPE).perform()

        # 3) Без приоритета
        create_btn = self.wait.until(EC.element_to_be_clickable(CREATE_TASK_BUTTON))
        create_btn.click()

        title_field = self.wait.until(EC.element_to_be_clickable(TITLE_FIELD))
        title_field.clear()
        title_field.send_keys("Задача без приоритета")

        project_field = self.wait.until(EC.element_to_be_clickable(PROJECT_FIELD))
        project_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_PROJECT)).click()

        assignee_field = self.wait.until(EC.element_to_be_clickable(ASSIGNE_FIELD))
        assignee_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_ASSIGNE)).click()

        self.assertTrue(is_button_disabled(), "Кнопка должна быть неактивна без приоритета")
        actions.send_keys(Keys.ESCAPE).perform()

        # 4) Без статуса (должна создаться)
        create_btn = self.wait.until(EC.element_to_be_clickable(CREATE_TASK_BUTTON))
        create_btn.click()

        title_field = self.wait.until(EC.element_to_be_clickable(TITLE_FIELD))
        title_field.clear()
        title_field.send_keys("Задача без статуса")

        project_field = self.wait.until(EC.element_to_be_clickable(PROJECT_FIELD))
        project_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_PROJECT)).click()

        priority_field = self.wait.until(EC.element_to_be_clickable(PRIORITY_FIELD))
        priority_field.click()
        self.wait.until(EC.element_to_be_clickable(LOW_PRIORITY)).click()

        assignee_field = self.wait.until(EC.element_to_be_clickable(ASSIGNE_FIELD))
        assignee_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_ASSIGNE)).click()

        self.assertTrue(is_button_enabled(), "Кнопка должна быть активна при заполнении всех полей")
        self.driver.find_element(*SUBMIT_BUTTON).click()
        time.sleep(2)

        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.clear()
        search_field.send_keys("Задача без статуса")
        time.sleep(2)

        task_in_list = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Задача без статуса')]")))
        self.assertTrue(task_in_list.is_displayed())

        # 5) Без исполнителя
        create_btn = self.wait.until(EC.element_to_be_clickable(CREATE_TASK_BUTTON))
        create_btn.click()

        title_field = self.wait.until(EC.element_to_be_clickable(TITLE_FIELD))
        title_field.clear()
        title_field.send_keys("Задача без исполнителя")

        project_field = self.wait.until(EC.element_to_be_clickable(PROJECT_FIELD))
        project_field.click()
        self.wait.until(EC.element_to_be_clickable(FIRST_PROJECT)).click()

        priority_field = self.wait.until(EC.element_to_be_clickable(PRIORITY_FIELD))
        priority_field.click()
        self.wait.until(EC.element_to_be_clickable(LOW_PRIORITY)).click()

        self.assertTrue(is_button_disabled(), "Кнопка должна быть неактивна без исполнителя")
        actions.send_keys(Keys.ESCAPE).perform()

    # TC003: Поиск по названию задачи
    def test_TC003_search_by_task_name(self):
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.clear()
        search_field.send_keys("ЗадачаДляПоиска")
        time.sleep(2)

        task_in_list = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'ЗадачаДляПоиска')]")))
        self.assertTrue(task_in_list.is_displayed())

    # TC004: Поиск по исполнителю
    def test_TC004_search_by_assignee(self):

        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.clear()
        search_field.send_keys("Илья Романов")
        time.sleep(2)

        # Ищем элементы с классом, содержащие информацию об исполнителе
        tasks_with_assignee = self.driver.find_elements(By.CLASS_NAME, "css-1xinhls")
        visible_tasks = [task for task in tasks_with_assignee if task.is_displayed()]

        self.assertTrue(len(visible_tasks) > 0)

    # TC005: Фильтрация по проекту через выпадающий список
    def test_TC005_filter_by_project(self):

        project_filter = self.wait.until(EC.element_to_be_clickable(PROJECT_FILTER))
        project_filter.click()
        time.sleep(1)

        redesign_project = self.wait.until(EC.element_to_be_clickable(REDESIGN_PROJECT))
        redesign_project.click()
        time.sleep(2)

        tasks = self.driver.find_elements(By.CLASS_NAME, "css-1xinhls")
        visible_tasks = [task for task in tasks if task.is_displayed()]
        self.assertTrue(len(visible_tasks) > 0)

    # TC006: Фильтрация по статусу через выпадающий список
    def test_TC006_filter_by_status(self):

        status_filter = self.wait.until(EC.element_to_be_clickable(STATUS_FILTER))
        status_filter.click()
        time.sleep(1)

        backlog_option = self.wait.until(EC.element_to_be_clickable(BACKLOG_STATUS))
        backlog_option.click()
        time.sleep(2)

        backlog_tasks = self.driver.find_elements(By.CSS_SELECTOR, ".MuiChip-labelSmall.css-b9zgoq")
        visible_backlog_tasks = [task for task in backlog_tasks if task.is_displayed() and task.text == "Backlog"]
        self.assertTrue(len(visible_backlog_tasks) > 0)

    # TC007: Комбинированная фильтрация (проект + статус)
    def test_TC009_combined_filtration(self):

        # Фильтруем по проекту "Редизайн карточки товара"
        project_filter = self.wait.until(EC.element_to_be_clickable(PROJECT_FILTER))
        project_filter.click()
        time.sleep(1)
        redesign_project = self.wait.until(EC.element_to_be_clickable(REDESIGN_PROJECT))
        redesign_project.click()
        time.sleep(1)

        # Фильтруем по статусу "Backlog"
        status_filter = self.wait.until(EC.element_to_be_clickable(STATUS_FILTER))
        status_filter.click()
        time.sleep(1)
        backlog_option = self.wait.until(EC.element_to_be_clickable(BACKLOG_STATUS))
        backlog_option.click()
        time.sleep(2)

        # Ищем видимые задачи после применения фильтров
        status_elements = self.driver.find_elements(By.CSS_SELECTOR, ".MuiChip-labelSmall.css-b9zgoq")
        visible_tasks = [elem for elem in status_elements if elem.is_displayed() and elem.text == "Backlog"]

        self.assertTrue(len(visible_tasks) > 0)

    # TC008: Поиск несуществующей задачи
    def test_TC008_search_nonexistent_task(self):

        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.clear()
        search_field.send_keys("НесуществующаяЗадача12345")
        time.sleep(2)

        no_tasks_message = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Задачи не найдены')]")))
        self.assertTrue(no_tasks_message.is_displayed())

    # TC009: Сброс фильтра 'Статус'
    def test_TC009_reset_status_filter(self):
        # Применяем фильтр по статусу "Backlog"
        status_filter = self.wait.until(EC.element_to_be_clickable(STATUS_FILTER))
        status_filter.click()
        time.sleep(1)
        backlog_option = self.wait.until(EC.element_to_be_clickable(BACKLOG_STATUS))
        backlog_option.click()
        time.sleep(1)

        # Сбрасываем фильтр, выбирая "Все"
        status_filter = self.wait.until(EC.element_to_be_clickable(STATUS_FILTER))
        status_filter.click()
        time.sleep(1)
        all_option = self.wait.until(EC.element_to_be_clickable(ALL_STATUS))
        all_option.click()
        time.sleep(1)

        # Проверяем, что задачи отображаются (фильтр сброшен)
        status_filter = self.wait.until(EC.element_to_be_clickable(STATUS_FILTER))
        status_filter_text = status_filter.text.strip()

        self.assertTrue(status_filter_text == "", "Фильтр статуса не сбросился")

    # TC010: Сброс фильтра 'Доска'
    def test_TC010_reset_project_filter(self):

        # Применяем фильтр по проекту "Редизайн карточки товара"
        project_filter = self.wait.until(EC.element_to_be_clickable(PROJECT_FILTER))
        project_filter.click()
        time.sleep(1)
        redesign_project = self.wait.until(EC.element_to_be_clickable(REDESIGN_PROJECT))
        redesign_project.click()
        time.sleep(1)

        # Сбрасываем фильтр, выбирая "Все"
        project_filter = self.wait.until(EC.element_to_be_clickable(PROJECT_FILTER))
        project_filter.click()
        time.sleep(1)
        all_option = self.wait.until(EC.element_to_be_clickable(ALL_PROJECTS))
        all_option.click()
        time.sleep(1)

        # Проверяем, что фильтр сбросился - текст должен быть пустым
        project_filter = self.wait.until(EC.element_to_be_clickable(PROJECT_FILTER))
        project_filter_text = project_filter.text.strip()

        self.assertTrue(project_filter_text == "", "Фильтр проекта не сбросился")

    # TC011: Поиск с частичным совпадением названия задачи
    def test_TC011_search_by_partial_task_name(self):
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.clear()
        search_field.send_keys("Поиска")
        time.sleep(2)

        task_in_list = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'ЗадачаДляПоиска')]")))
        self.assertTrue(task_in_list.is_displayed())

    # TC012: Поиск с частичным совпадением исполнителя задачи
    def test_TC012_search_by_partial_assignee(self):
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.clear()
        search_field.send_keys("Романов")
        time.sleep(2)

        tasks = self.driver.find_elements(By.CLASS_NAME, "css-1xinhls")
        visible_tasks = [task for task in tasks if task.is_displayed()]

        self.assertTrue(len(visible_tasks) > 0)

    # TC013: Открытие и проверка полей существующей задачи
    def test_TC013_open_existing_task_card(self):
        task_title = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        # Проверяем, что все поля отображаются и заполнены правильными значениями
        title_field = self.driver.find_element(*TITLE_FIELD)
        description_field = self.driver.find_element(*DESCRIPTION_FIELD)
        project_field = self.driver.find_element(*PROJECT_FIELD)
        priority_field = self.driver.find_element(*PRIORITY_FIELD)
        status_field = self.driver.find_element(*STATUS_FIELD)
        assignee_field = self.driver.find_element(*ASSIGNE_FIELD)

        # Проверяем отображение полей
        self.assertTrue(title_field.is_displayed())
        self.assertTrue(description_field.is_displayed())
        self.assertTrue(project_field.is_displayed())
        self.assertTrue(priority_field.is_displayed())
        self.assertTrue(status_field.is_displayed())
        self.assertTrue(assignee_field.is_displayed())

        # Проверяем значения полей
        self.assertEqual(title_field.get_attribute("value"), "Адаптация карточки для мобильных устройств")
        self.assertEqual(description_field.get_attribute("value"), "Обновленное описание задачи")
        self.assertEqual(project_field.text.strip(), "Редизайн карточки товара")
        self.assertEqual(priority_field.text.strip(), "Medium")
        self.assertEqual(status_field.text.strip(), "InProgress")
        self.assertEqual(assignee_field.text.strip(), "Илья Романов")

    # TC014: Навигация из карточки задачи на доску проекта
    def test_TC014_navigate_to_board_from_task_card(self):
        task_title = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Адаптация карточки')]")))
        task_title.click()
        time.sleep(1)

        # Используем новый локатор для кнопки "Перейти на доску"
        board_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Перейти на доску')]")))
        board_btn.click()
        time.sleep(2)

        self.wait.until(EC.url_contains("/board"))
        self.assertIn("/board", self.driver.current_url)

    # TC015: Обновление данных в карточке задачи
    def test_TC015_update_task_data(self):
        task_title = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Адаптация карточки')]")))
        task_title.click()
        time.sleep(1)

        update_btn = self.wait.until(EC.element_to_be_clickable(UPDATE_BUTTON))
        update_btn.click()
        time.sleep(1)

        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))

    # TC016: Редактирование задачи через карточку (поочередная проверка всех полей)
    def test_TC016_edit_task_through_card(self):
        # 1) Редактирование описания
        # Сначала находим задачу через поиск
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        description_field = self.wait.until(EC.element_to_be_clickable(DESCRIPTION_FIELD))

        # Физическое взаимодействие с полем: выделить все, удалить, ввести новое
        description_field.click()
        description_field.send_keys(Keys.CONTROL + "a")
        description_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        description_field.send_keys("Обновленное описание задачи")
        time.sleep(1)

        update_btn = self.wait.until(EC.element_to_be_clickable(UPDATE_BUTTON))
        update_btn.click()
        time.sleep(2)
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))

        # Проверяем через поиск, что описание изменилось
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        description_field = self.wait.until(EC.element_to_be_clickable(DESCRIPTION_FIELD))
        self.assertEqual(description_field.get_attribute("value"), "Обновленное описание задачи")

        # Закрываем карточку
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        # 2) Редактирование приоритета
        # Снова находим задачу через поиск
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        priority_field = self.wait.until(EC.element_to_be_clickable(PRIORITY_FIELD))
        priority_field.click()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(MEDIUM_PRIORITY)).click()
        time.sleep(1)

        update_btn = self.wait.until(EC.element_to_be_clickable(UPDATE_BUTTON))
        update_btn.click()
        time.sleep(2)
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))

        # Проверяем через поиск, что приоритет изменился
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        priority_field = self.wait.until(EC.element_to_be_clickable(PRIORITY_FIELD))
        self.assertEqual(priority_field.text.strip(), "Medium")

        # Закрываем карточку
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        # 3) Редактирование статуса
        # Снова находим задачу через поиск
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        status_field = self.wait.until(EC.element_to_be_clickable(STATUS_FIELD))
        status_field.click()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(IN_PROGRESS_STATUS)).click()
        time.sleep(1)

        update_btn = self.wait.until(EC.element_to_be_clickable(UPDATE_BUTTON))
        update_btn.click()
        time.sleep(2)
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))

        # Проверяем через поиск, что статус изменился
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        status_field = self.wait.until(EC.element_to_be_clickable(STATUS_FIELD))
        self.assertEqual(status_field.text.strip(), "InProgress")

        # Закрываем карточку
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        # 4) Редактирование исполнителя
        # Снова находим задачу через поиск
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        assignee_field = self.wait.until(EC.element_to_be_clickable(ASSIGNE_FIELD))
        assignee_field.click()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(SECOND_ASSIGNEE)).click()
        time.sleep(1)

        update_btn = self.wait.until(EC.element_to_be_clickable(UPDATE_BUTTON))
        update_btn.click()
        time.sleep(2)
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))

        # Проверяем через поиск, что исполнитель изменился
        search_field = self.wait.until(EC.element_to_be_clickable(SEARCH_FIELD))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_field.send_keys("Адаптация карточки для мобильных устройств")
        time.sleep(2)

        task_title = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Адаптация карточки для мобильных устройств')]")))
        task_title.click()
        time.sleep(1)

        assignee_field = self.wait.until(EC.element_to_be_clickable(ASSIGNE_FIELD))
        new_assignee = assignee_field.text.strip()
        self.assertEqual(new_assignee, "Илья Романов")
        # Закрываем карточку
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

    # TC017: Закрытие карточки задачи
    def test_TC017_close_task_card(self):
        task_title = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Адаптация карточки')]")))
        task_title.click()
        time.sleep(1)

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))

    # TC018: Открытие разных задач по очереди
    def test_TC018_open_different_tasks_sequentially(self):
        first_task = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Адаптация карточки')]")))
        first_task.click()
        time.sleep(1)

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        second_task = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Реализация новой галереи')]")))
        second_task.click()
        time.sleep(1)

        self.assertTrue(self.driver.find_element(*TITLE_FIELD).is_displayed())

    # TC019: Переход на доску проекта через список проектов
    def test_TC019_go_to_project_board_via_projects_list(self):
        projects_tab = self.wait.until(EC.element_to_be_clickable(PROJECTS_TAB))
        projects_tab.click()
        time.sleep(2)

        board_btn = self.wait.until(EC.element_to_be_clickable(GO_TO_BOARD_BUTTON_4))
        board_btn.click()
        time.sleep(2)

        self.wait.until(EC.url_contains("/board/4"))
        current_url = self.driver.current_url
        self.assertIn("/board/4", current_url)

    # TC020: Переход на доску проекта через карточку задачи
    def test_TC020_go_to_board_from_task_card(self):
        task_title = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Адаптация карточки')]")))
        task_title.click()
        time.sleep(1)

        board_btn = self.wait.until(EC.element_to_be_clickable(GO_TO_BOARD_BUTTON))
        board_btn.click()
        time.sleep(2)

        self.wait.until(EC.url_contains("/board"))
        self.assertIn("/board", self.driver.current_url)

    # TC021: Проверка структуры доски проекта
    def test_TC021_check_project_board_structure(self):
        self.test_TC019_go_to_project_board_via_projects_list()

        todo_column = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'To Do')]")))
        in_progress_column = self.driver.find_element(By.XPATH, "//*[contains(text(), 'In Progress')]")
        done_column = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Done')]")

        self.assertTrue(todo_column.is_displayed())
        self.assertTrue(in_progress_column.is_displayed())
        self.assertTrue(done_column.is_displayed())

        task_cards = self.driver.find_elements(By.CSS_SELECTOR, ".MuiCard-root")
        self.assertTrue(len(task_cards) > 0)

    # TC022: Проверка отображения информации о задачах на доске
    def test_TC022_check_task_info_on_board(self):
        self.test_TC019_go_to_project_board_via_projects_list()

        task_titles = self.driver.find_elements(By.CSS_SELECTOR, ".MuiTypography-subtitle1")
        task_descriptions = self.driver.find_elements(By.CSS_SELECTOR, ".MuiTypography-body2")
        task_assignees = self.driver.find_elements(By.CSS_SELECTOR, ".MuiChip-labelSmall")

        self.assertTrue(len(task_titles) > 0)
        self.assertTrue(len(task_descriptions) > 0)
        self.assertTrue(len(task_assignees) > 0)

    # TC023: Переход между разными досками проектов
    def test_TC023_switch_between_project_boards(self):
        # 1) Переходим на страницу проектов
        projects_tab = self.wait.until(EC.element_to_be_clickable(PROJECTS_TAB))
        projects_tab.click()
        time.sleep(2)

        # Проверяем, что мы на странице проектов
        self.wait.until(EC.url_contains("/boards"))

        # 2) Переходим на первый проект (Редизайн карточки товара)
        first_project_board = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/board/1']")))
        first_project_board.click()
        time.sleep(2)

        # Проверяем, что мы на доске первого проекта
        self.wait.until(EC.url_contains("/board/1"))
        first_board_url = self.driver.current_url

        # 3) Возвращаемся на страницу проектов через кнопку "Проекты"
        projects_tab = self.wait.until(EC.element_to_be_clickable(PROJECTS_TAB))
        projects_tab.click()
        time.sleep(2)

        # Проверяем, что мы вернулись на страницу проектов
        self.wait.until(EC.url_contains("/boards"))

        # 4) Переходим на второй проект (Оптимизация производительности)
        second_project_board = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/board/2']")))
        second_project_board.click()
        time.sleep(2)

        # Проверяем, что мы на доске второго проекта
        self.wait.until(EC.url_contains("/board/2"))
        second_board_url = self.driver.current_url

        # Проверяем, что это разные доски
        self.assertNotEqual(first_board_url, second_board_url, "URL досок должны отличаться")

    # TC024: Проверка навигации с доски проекта
    def test_TC024_check_navigation_from_board(self):
        # 1) Переходим на страницу проектов
        print("Шаг 1: Переход на страницу проектов")
        projects_tab = self.wait.until(EC.element_to_be_clickable(PROJECTS_TAB))
        projects_tab.click()
        time.sleep(2)

        # Проверяем, что мы на странице проектов
        self.assertIn("/boards", self.driver.current_url)

        # 2) Переходим на доску проекта
        first_board_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/board/1']")))
        first_board_btn.click()
        time.sleep(2)

        # Проверяем, что мы на доске проекта
        self.assertIn("/board/1", self.driver.current_url)
        print("✓ Успешно перешли на доску проекта")

        # 3) Переходим на вкладку "Все задачи"
        all_tasks_btn = self.wait.until(EC.element_to_be_clickable(ALL_TASKS_BUTTON))
        all_tasks_btn.click()
        time.sleep(2)

        # Проверяем, что мы перешли на страницу со всеми задачами
        self.wait.until(EC.url_contains("/issues"))
        self.assertIn("/issues", self.driver.current_url)

if __name__ == "__main__":
    unittest.main(verbosity=2)