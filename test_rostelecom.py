import pytest

from auth_page import AuthPage
from registration_page import RegPage


# Проверка элементов в левом и правом блоке страницы
@pytest.mark.xfail(reason="Расположение элементов на странице не соответсвует ожидаемым требованиям")
def test1_location_of_page_blocks(web_browser):
    page = AuthPage(web_browser)
    assert page.auth_form.find(timeout=1)
    assert page.lk_form.find(timeout=1)

# Проверка таб выбора "Номер"
@pytest.mark.xfail(reason="Таб выбора 'Номер' не соответсвует ожидаемым требованиям")
def test2_phone_tab(web_browser):
    page = AuthPage(web_browser)
    assert page.phone_tab.get_text() == "Номер"

# Проверка название кнопки "Продолжить" в форме "Регистрация"
@pytest.mark.xfail(reason="Кнопка должна иметь текст 'Продолжить'")
def test3_registration_page_and_continue_button(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    assert reg_page.name_field_text.get_text() == "Имя"
    assert reg_page.last_name_field_text.get_text() == "Фамилия"
    assert reg_page.region_field_text.get_text() == "Регион"
    assert reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон"
    assert reg_page.password_field_text.get_text() == "Пароль"
    assert reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля"
    assert reg_page.continue_button.get_text() == "Продолжить"

# Регистрация пользователя с пустым полем "Имя", появления текста с подсказкой об ошибке
def test4_registration_page_with_empty_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('')
    reg_page.last_name_field.send_keys("Фамилия")
    reg_page.email_or_mobile_phone_field.send_keys("123@mail.ru")
    reg_page.password_field.send_keys("Qwwww12!")
    reg_page.password_confirmation_field.send_keys("Qwwww12!")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."

# Регистрация пользователя с некорректным значением в поле "Имя"(< 2 символов), появление текста с подсказкой об ошибке
def test5_registration_with_an_incorrect_value_in_the_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('р')
    reg_page.last_name_field.send_keys("Фамилия")
    reg_page.email_or_mobile_phone_field.send_keys("123@mail.ru")
    reg_page.password_field.send_keys("Qwwww12!")
    reg_page.password_confirmation_field.send_keys("Qwwww12!")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."

# Регестрация пользователя с некорректным значением в поле "Фамилия"(>30 символов), появление текста с подскаской об ошибке
def test6_registration_with_an_incorrect_value_in_the_last_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Иван")
    reg_page.last_name_field.send_keys("Володывалодваллаоывннаыдвалоаывареткр")
    reg_page.email_or_mobile_phone_field.send_keys("123@mail.ru")
    reg_page.password_field.send_keys("Qwwww12!")
    reg_page.password_confirmation_field.send_keys("Qwwww12!")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."

# Регистрация пользователя с уже зарегистрированным номером, отображается оповещающая форма
def test7_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Иван")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("+79000000001")
    reg_page.password_field.send_keys("123@mail.ru")
    reg_page.password_confirmation_field.send_keys("123456")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible

# Проверка кнопки "х" - закрыть всплывающее окно оповещения
@pytest.mark.xfail(reason="Должна быть кнопка закрыть 'х'")
def test8_notification_form(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Иван")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("+79000000001")
    reg_page.password_field.send_keys("123456")
    reg_page.password_confirmation_field.send_keys("123456")
    reg_page.continue_button.click()
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'

# Некорректный пароль при регистрации пользователя(< 8 символов), появления текста с подсказкой об ошибке
def test9_incorrect_password_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Иван")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("123@mail.ru")
    reg_page.password_field.send_keys("Zx!1")
    reg_page.password_confirmation_field.send_keys("Zx!1")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"

# Вход по неправильному паролю в форме "Авторизация" уже зарегистрированного пользователя, появляется надпись "Забыл пароль"
def test10_authorization_of_a_user_with_an_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79000000001')
    page.password.send_keys("Test")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"

# в поле ввода "Фамилия" вместо кириллицы, недопустимые символы
def test11_instead_of_cyrillic_invalid_characters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Иван")
    reg_page.last_name_field.send_keys("@@@@!!!")
    reg_page.email_or_mobile_phone_field.send_keys("123@mail.ru")
    reg_page.password_field.send_keys("Qwwww12!")
    reg_page.password_confirmation_field.send_keys("Qwwww12!")
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."

# Поле ввода "Пароль" и поле ввода "Подтверждение пароля"  в форме "Регистрация" не совпадают
def test12_password_and_password_confirmation_not_match(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Иван")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("123@mail.ru")
    reg_page.password_field.send_keys("Qwwww12!")
    reg_page.password_confirmation_field.send_keys("Qwwww121!")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"

# Не валидный email в поле ввода "Email или мобильный телефон"
def test13_invalid_email_or_mobile_phone(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Иван")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("10000000")
    reg_page.password_field.send_keys("Qwwww12!")
    reg_page.password_confirmation_field.send_keys("Qwwww12!")
    reg_page.continue_button.click()
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email в формате example@email.ru"
# Тестирование аутентификации зарегестрированного пользователя
def test14_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('valid_phone')
    page.password.send_keys("valid_password")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()

# Проверка перехода на страницу с описанием политики конфиденциальности
def test15_auth_privacy_policy_page(web_browser):

    page = AuthPage(web_browser)
    page.privacy_policy_button.click()
    page.switch_to_new_window()
    page.screenshot('test15.jpg')

    assert 'private' in page.get_current_url()
    assert 'agreement' not in page.get_current_url()