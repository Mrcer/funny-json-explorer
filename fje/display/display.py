from abc import ABC, abstractmethod
from ..node import JSONNode
from ..icon import IconFamily

"""
策略接口：用于显示JSONNode
"""
class DisplayStrategy(ABC):

    @abstractmethod
    def display(self, root: JSONNode, icon_family: IconFamily) -> None:
        pass