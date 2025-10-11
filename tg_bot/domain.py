from pydantic import BaseModel


class Config(BaseModel):
    height: float
    width: float
    length: float
    weight: float

    @property
    def volume(self):
        return self.height * self.width * self.length


class Calculator:
    def calculate(self, height, width, length, config: Config) -> float:
        volume = height * width * length
        # Немає ніякого сенсу погіршувати точність округленням типу float,
        # кількість знаків після коми - це задача виводу/форматування.
        return volume / config.volume * config.weight


class ConfigManager:
    def __init__(self):
        self.data = {}

    async def get(self, key) -> Config | None:
        return self.data.get(key)

    async def set(self, key, config: Config):
        self.data[key] = config
