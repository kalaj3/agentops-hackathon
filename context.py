from openai import BaseModel


class AgentContext(BaseModel):
    """Global state of the system"""

    disaster_info: str
    """Information gathered about the disaster"""



    i_news: int = 0

