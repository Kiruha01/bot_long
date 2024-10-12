import asyncio
import hashlib

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from loguru import logger

from app.examer.exception import (
    EmailPasswordError,
    GettingTestError,
    LoginError,
    SignError,
    TeacherError,
)
from app.examer.schemas import ExamerTest
from app.settings import settings


class ExamerController:
    def __init__(self) -> None:
        self.MAX_REQUESTS = 20
        self.SIGN_POSTFIX = "Ic8_31"
        self.BASE_URL = "https://examer.ru/"
        self.client = ClientSession(
            base_url=self.BASE_URL,
            headers={"Referer": self.BASE_URL},
        )

    async def check_auth(self) -> bool:
        async with self.client.get("/api/v2/user") as resp:
            logger.info(f"Check Examer auth: {resp.status}")
            resp_data = await resp.json()
            if not resp_data.get("profile", {}).get("is_teacher"):
                logger.error("User is not teacher")
                return False

        return True

    async def auth(
        self, email: str = settings.EMAIL, password: str = settings.PASSWORD
    ):
        """
        Метод входа в аккаунт
        :param email: str
        :param password: str
        :return: None

        :raises EmailPasswordError: неверный логин или пароль
        :raises LoginError: неопознанная ошибка входа
        :raises SignError: ошибка отправки запроса регистрации
        :raises TeacherError: пользователь не является учителем
        """
        logger.info(f"LogIn to Examer as {email[:3]}...{email[-5:]}")
        async with self.client.get("/") as resp:
            if resp.status != 200:
                logger.error(f"Examer error response: {resp.status}")
                logger.error(await resp.text())
                raise LoginError()

            soup = BeautifulSoup(await resp.text(), "html.parser")

        token = soup.find(id="login-form").find("input", attrs={"name": "_token"})[
            "value"
        ]
        params = self._prepare_auth_request_params(email, password, token)

        async with self.client.post("/api/v2/login", data=params) as resp:
            resp_data = await resp.json()
            if not resp_data.get("success"):
                logger.error(f"Examer error: {resp_data}")
                if resp_data.get("error") == 3:
                    logger.error("Wrong email or password")
                    raise EmailPasswordError()
                elif resp_data.get("error") == 101:
                    logger.error("Sign error")
                    raise SignError()
                else:
                    logger.error("Something went wrong. Login error")
                    raise LoginError()

        async with self.client.get("/api/v2/user") as resp:
            resp_data = await resp.json()
            if not resp_data.get("profile", {}).get("is_teacher"):
                logger.error("User is not teacher")
                raise TeacherError()

        logger.info(f"Login as {email[:3]}...{email[-5:]} success")

    async def get_questions(self, test_id: str) -> ExamerTest:
        """
        Получение вопросов теста.
        :param test_id: str - идентификатор теста из ссылки
        :return: ExamerText
        """
        logger.info(f"Get questions from {test_id}")
        async with self.client.get("/api/v2/teacher/test/student/" + test_id) as resp:
            if resp.status != 200:
                logger.error(f"Examer error response: {resp.status}")
                logger.error(await resp.text())
                raise GettingTestError()

            resp_data = await resp.json()
            if "error" in resp_data:
                logger.error(resp_data["error"])
                raise GettingTestError()

        test = ExamerTest(resp_data.get("test"))
        logger.info(f"For test {test_id} got {len(test.tasks)} questions")
        return test

    async def process_link(self, link: str) -> ExamerTest:
        """
        Метод получения ответов на тест по ссылке.
        :param link: str - ссылка на тест
        :return: ExamerTest
        """
        test_id = link.split("/")[-1]
        test = await self.get_questions(test_id)

        tasks = [self._insert_answers_async(test) for _ in range(self.MAX_REQUESTS)]

        await asyncio.gather(*tasks, return_exceptions=True)
        return test

    async def _insert_answers_async(self, test: ExamerTest):
        payload = {
            "sid": test.sid,
            "scenario": test.scenario,
            "id": test.scenarioId,
            "title": test.theme,
            "easy": "12",
            "normal": "12",
            "hard": "12",
        }

        async with self.client.post("/api/v2/teacher/test", data=payload) as resp:
            data = await resp.json()
            for task in data.get("tasks", []):
                if task["id"] in test.unprocessed_tasks_id:
                    test.tasks[task["id"]].answer = task["answer"]
                    test.unprocessed_tasks_id.remove(task["id"])

            if len(test.unprocessed_tasks_id) == 0:
                raise StopIteration

    def _prepare_auth_request_params(
        self, email: str, password: str, token: str
    ) -> dict[str, str]:
        """
        Подготовка параметров для регистрации и добавление подписи.
        :param email: str - email для входа
        :param password: str - пароль для входа
        :param token: str - токен с формы регистрации
        :return: Dict[str, str]
        """
        data = {
            "_mail": email,
            "_pass": password,
            "_token": token,
            "source_reg": "login_popup",
        }
        string = "".join(sorted(data.values())) + self.SIGN_POSTFIX
        data["s"] = hashlib.md5(string.encode("utf-8")).hexdigest()
        return data


controller = ExamerController()
