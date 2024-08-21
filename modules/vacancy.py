class Vacancy:
    def __init__(self, team_id: str, hardskill: str, specialization: str) -> None:
        self.__team_id = team_id
        self.__hardskill = hardskill.split(",")
        self.__specialization = specialization

    @property
    def team_id(self) -> str:
        return self.__team_id

    @property
    def hardskill(self) -> list[str]:
        return self.__hardskill

    @property
    def specialization(self) -> str:
        return self.__specialization

    @property
    def hardskill_str(self) -> str:
        return ",".join(self.__hardskill)

    def get_dict(self) -> dict:
        return {
            "team_id": self.team_id,
            "hardskill": self.hardskill_str,
            "specialization": self.specialization,
        }
