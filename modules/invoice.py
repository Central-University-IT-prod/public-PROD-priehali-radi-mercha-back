class Invoice:

    def __init__(
        self,
        owner_id: str,
        team_id: str,
        invoice_type: str,
        specialization: str,
        date: str,
    ) -> None:
        self.__owner_id = owner_id
        self.__team_id = team_id
        self.__invoice_type = invoice_type
        self.__specialization = specialization
        self.__date = date

    @property
    def owner_id(self) -> str:
        return self.__owner_id

    @property
    def team_id(self) -> str:
        return self.__team_id

    @property
    def invoice_type(self) -> str:
        return self.__invoice_type

    @property
    def specialization(self) -> str:
        return self.__specialization

    @property
    def date(self) -> str:
        return self.__date

    def to_dict(self) -> dict:
        return {
            "owner_id": self.owner_id,
            "team_id": self.team_id,
            "invoice_type": self.invoice_type,
            "specialization": self.specialization,
            "date": self.date,
        }
