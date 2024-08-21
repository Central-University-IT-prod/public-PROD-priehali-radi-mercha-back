class Organization:
    def __init__(self,
                 org_id: str,
                 title: str,
                 description: str,
                 owner: str) -> None:
        self.__org_id = org_id
        self.__title = title
        self.__description = description
        self.__owner = owner

    @property
    def org_id(self) -> str:
        return self.__org_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def owner(self) -> str:
        return self.__owner

    def get_dict(self) -> dict:
        return {
            "org_id": self.__org_id,
            "title": self.__title,
            "description": self.__description,
            "owner": self.__owner
        }
