"""
sample output:
┌─+name1 ───────────────┐
│  ├─*name2 ────────────┤
│  ├─+name3 ────────────┤
│  │  ├─*name4: value4 ─┤
└─*name5 ───────────────┘

设计模式：
1. 工厂模式：StyledJSONNodeFactory
"""
from .style import StyledJSONNode, StyledJSONNodeFactory
from ..node import *
from ..icon import IconFamily

class FirstLastDetector:

    def __init__(self, root: JSONNode):
        self.first_visited = False
        root.traverse(lambda node: self.fn(node))

    def fn(self, node: JSONNode):
        if node.is_root():
            return
        if not self.first_visited:
            self.first_visited = True
            self.first_id = node.get_id()
        else:
            self.last_id = node.get_id()

    def is_first(self, node: JSONNode) -> bool:
        return node.get_id() == self.first_id
    
    def is_last(self, node: JSONNode) -> bool:
        return node.get_id() == self.last_id

class RectangleStyledJSONNode(StyledJSONNode):

    def __init__(self, root: JSONNode, icon_family: IconFamily):
        super().__init__(root, icon_family)
        self._grid_width = 16
        self._root.traverse(lambda node: self._update_grid_width(node))
        self.fl_detector = FirstLastDetector(root)
        
    def _update_grid_width(self, node: JSONNode) -> None:
        prefix_length = max((node.get_level() - 1) * 3 + 2, 0)
        name_length = len(node.get_name()) + 2
        if node.is_leaf() and node.get_value() is not None:
            name_length += len(node.get_value()) + 2
        self._grid_width = max(self._grid_width, prefix_length + name_length + 2)
    
    def render(self) -> None:
        self._root.traverse(lambda node: self._render(node))

    def _render(self, node: JSONNode) -> None:
        if node.is_root():
            return
        result = ''
        # first layer
        if self.fl_detector.is_first(node):
            result += "┌─"
        elif self.fl_detector.is_last(node):
            result += "└─"
        elif node.get_level() == 1:
            result += "├─"
        else:
            result += "│ "
        # straight lines
        if node.get_level() > 2:
            if self.fl_detector.is_last(node):
                result += '─┴─' * (node.get_level() - 2)
            else:
                result += ' │ ' * (node.get_level() - 2)
        # header
        if self.fl_detector.is_last(node):
            result += '─┴─'
        elif node.get_level() > 1:
            result += ' ├─'
        # icon
        if node.is_leaf():
            result += self._icon_family.leaf_icon
        else:
            result += self._icon_family.composite_icon
        # name
        result += node.get_name()
        # value
        if node.is_leaf() and node.get_value() is not None:
            result += f': {node.get_value()}'
        # padding
        result = f'{result} '.ljust(self._grid_width - 2, '─')
        # last layer
        if self.fl_detector.is_first(node):
            result += '─┐'
        elif self.fl_detector.is_last(node):
            result += '─┘'
        else:
            result += '─┤'
        print(result)

class RectangleStyledJSONNodeFactory(StyledJSONNodeFactory):

    def create(self, root: JSONNode, icon_family: IconFamily) -> StyledJSONNode:
        return RectangleStyledJSONNode(root, icon_family)