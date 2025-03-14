from openai import BaseModel


class AgentContext(BaseModel):
    """Global state of the system"""

    confirmation_number: str = ""
    flight_number: str = ""
    seat_number: str = ""

