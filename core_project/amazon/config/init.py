import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../core'))

from core_project.core.config.init import Config as CoreConfig


class Config(CoreConfig):
    """Amazon specific configuration extending core config"""

    def __init__(self, environment: str = "dev"):
        super().__init__(environment, config_path="amazon/config")

    @property
    def search_term(self) -> str:
        return self.get('search_term', 'samsung smartphone')

    @property
    def min_price(self) -> float:
        return self.get('min_price', 100)

    @property
    def max_price(self) -> float:
        return self.get('max_price', 1000)

    @property
    def items_to_add(self) -> int:
        return self.get('items_to_add', 2)