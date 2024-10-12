class ExamerException(Exception):
    pass


class LoginError(ExamerException):
    def __init__(self):
        self.message = "Неопознанная ошибка регистрации"
        super().__init__(self.message)


class EmailPasswordError(ExamerException):
    def __init__(self):
        self.message = "Неверный email или пароль"
        super().__init__(self.message)


class GettingTestError(ExamerException):
    def __init__(self):
        self.message = "Ошибка в получении теста"
        super().__init__(self.message)


class SignError(ExamerException):
    def __init__(self):
        self.message = "Ошибка генерации запроса регистрации"
        super().__init__(self.message)


class TeacherError(ExamerException):
    def __init__(self):
        self.message = "Пользователь не является учителем"
        super().__init__(self.message)
