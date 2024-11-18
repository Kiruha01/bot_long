from bs4 import BeautifulSoup


class Task:
    """
    Структура, описывающая задание

    :field id: str - ID задания
    :field question: str - текст задания
    :field difficult: int - баллы за задание (1, 2 или 3)
    :field avg_time: float - время на выполнение
    :field answer: str - правильный ответ

    """

    def __init__(self, task_dict: dict[str, str]):
        self.id: str = task_dict.get("id")
        self.question: str = self.__remove_tags(task_dict["task_text"])
        self.difficult: int = self.__convert_dif(task_dict["difficult"])
        self.avg_time: float = float(task_dict["avg_time"])
        self.answer = "No answer"

    @staticmethod
    def __remove_tags(text: str) -> str:
        soup = BeautifulSoup(text, "html.parser")
        return soup.text

    @staticmethod
    def __convert_dif(grade: str) -> int:
        if grade == "easy":
            return 1
        elif grade == "normal":
            return 2
        else:
            return 3

    @property
    def formatted_question(self) -> str:
        return (
            f"{'🌚' * self.difficult}\n```\n{self.question}\n```\n\n" f"Ответ: `{self.answer}`"
        )


class ExamerTest:
    """
    Структура, описывающая тест

    :field theme: str - тема теста
    :field score: str - возможное количество баллов за тест
    :field tasks: Dist[str, Task] - словарь заданий вида ("task_id": Task)
    :field avg_time: int - примерное время выполнения теста
    """

    def __init__(self, test_dict: dict):
        self.theme: str = test_dict["title"]
        self.scenarioId: int = test_dict["scenarioId"]
        self.scenario: int = test_dict["scenario"]
        self.sid: int = test_dict["subject"]["id"]
        self.score: str = str(test_dict["score"])
        self.tasks: dict[str, Task] = {}
        self.avg_time = 0
        for task in test_dict["tasks"]:
            t = Task(task)
            self.tasks[t.id] = t
            self.avg_time += t.avg_time
        self.unprocessed_tasks_id: list[str] = list(self.tasks.keys())

        self.avg_time = round(self.avg_time / 30)

    def get_tasks(self) -> list[Task]:
        """
        Получить список вопросов
        :return: List[Task]
        """
        return list(self.tasks.values())
