from typing import Optional


class User:
    def __init__(
        self,
        login: str,
        password: str,
        username: Optional[str],
        telegram: str,
        user_type: Optional[str],
        hardskill: Optional[str],
        softskill: Optional[str],
        role: str,
        specialization: Optional[str] = None,
        description: Optional[str] = None,
        picture: Optional[str] = None,
    ) -> None:
        self.__login = login
        self.__password = password
        self.__username = username
        self.__telegram = telegram
        self.__type = user_type
        self.__hardskill = hardskill.split(",") if hardskill is not None else None
        self.__softskill = softskill.split(",") if softskill is not None else None
        self.__role = role
        self.__description = description
        self.__picture = picture
        self.__specialization = specialization

    @property
    def login(self) -> str:
        return self.__login

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, new_password: str) -> None:
        self.__password = new_password

    @property
    def username(self) -> Optional[str]:
        return self.__username

    @username.setter
    def username(self, new_username: str) -> None:
        self.__username = new_username

    @property
    def telegram(self) -> str:
        return self.__telegram

    @telegram.setter
    def telegram(self, new_telegram: str) -> None:
        self.__telegram = new_telegram

    @property
    def user_type(self) -> Optional[str]:
        return self.__type

    @user_type.setter
    def user_type(self, new_type: str) -> None:
        self.__type = new_type

    @property
    def hardskill(self) -> Optional[list[str]]:
        return self.__hardskill

    @hardskill.setter
    def hardskill(self, new_hardskill: list[str]) -> None:
        self.__hardskill = new_hardskill

    @property
    def softskill(self) -> Optional[list[str]]:
        return self.__softskill

    @softskill.setter
    def softskill(self, new_softskill: list[str]) -> None:
        self.__softskill = new_softskill

    @property
    def role(self) -> str:
        return self.__role

    @role.setter
    def role(self, new_role: str) -> None:
        self.__role = new_role

    @property
    def description(self) -> Optional[str]:
        return self.__description

    @description.setter
    def description(self, new_description: str) -> None:
        self.__description = new_description

    @property
    def picture(self) -> Optional[str]:
        return self.__picture

    @picture.setter
    def picture(self, new_picture: str) -> None:
        self.__picture = new_picture

    @property
    def specialization(self) -> Optional[str]:
        return self.__specialization

    @specialization.setter
    def specialization(self, new_specialization: str) -> None:
        self.__specialization = new_specialization

    def get_dict(self) -> dict:
        return {
            "login": self.__login,
            "username": self.__username,
            "telegram": self.__telegram,
            "type": self.__type,
            "hardskill": self.__hardskill,
            "softskill": self.__softskill,
            "role": self.__role,
            "description": self.__description,
            "specialization": self.__specialization,
        }

    def get_str_softskills(self) -> Optional[str]:
        if self.__softskill is None:
            return None
        return ",".join(self.__softskill)

    def get_str_hardskills(self) -> Optional[str]:
        if self.__hardskill is None:
            return None
        return ",".join(self.__hardskill)
