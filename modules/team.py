from typing import Optional

from database.vacancies_database import VacanciesDatabase


def get_hardskills(team_id):
    vanacys = VacanciesDatabase('none').get_vacancies(team_id)
    hardskills = ""
    for i in range(len(vanacys)):
        hardskills += vanacys[i]['hardskill']
        if i != len(vanacys) - 1:
            hardskills += ","
    return hardskills


class Team:
    def __init__(
            self,
            team_id: str,
            owner: str,
            name: str,
            created_at: str,
            max_participants: int = 3,
            hardskills: str = None,
            description: str = ''
    ) -> None:
        self.__team_id: str = team_id
        self.__owner: str = owner
        self.__name: str = name
        self.__created_at: str = created_at
        self.__max_participants = max_participants
        self.__description = description
        if hardskills is None or hardskills.strip() == '':
            self.__hardskills = get_hardskills(team_id)
        else:
            self.__hardskills = hardskills

    @property
    def team_id(self) -> str:
        return self.__team_id

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def name(self) -> str:
        return self.__name

    @property
    def created_at(self) -> str:
        return self.__created_at

    @property
    def created_at_str(self) -> str:
        return self.__created_at

    @property
    def max_participants(self) -> int:
        return self.__max_participants

    @property
    def hardskills(self) -> str:
        return self.__hardskills

    @property
    def description(self) -> str:
        return self.__description

    def get_hardskills_str(self) -> Optional[str]:
        if self.__hardskills is None:
            return ""
        return ",".join(self.__hardskills)

    def get_dict(self, mode: str = "str") -> dict:
        return {
            "team_id": self.team_id,
            "owner": self.owner,
            "name": self.name,
            "created_at": self.created_at,
            "max_participants": self.max_participants,
            "hardskills": self.hardskills,
            "description": self.description
        }
