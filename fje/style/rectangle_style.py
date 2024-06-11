"""
sample output:
┌─+name1 ───────────────┐
│  ├─*name2 ────────────┤
│  ├─+name3 ────────────┤
│  │  ├─*name4: value4 ─┤
└─*name5 ───────────────┘

设计模式：
1. 策略模式：DisplayRectangleStyle 继承自 DisplayStrategy，是策略模式的具体实现。
"""
from .display import DisplayStrategy
from ..node import *
from ..icon import IconFamily    

class DisplayRectangleStyle(DisplayStrategy):

    def __init__(self) -> None:
        # placeholder
        self._grid_width = 0

    def display(self, root: JSONNode, icon_family: IconFamily) -> None:
        self._update_grid_width(root)
        all_nodes = list(root)
        # 根节点不渲染
        all_nodes.pop(0)
        self._render_node(all_nodes[0], True, False, icon_family)
        for i in all_nodes[1:-1]:
            self._render_node(i, False, False, icon_family)
        if len(all_nodes) > 1:
            self._render_node(all_nodes[-1], False, True, icon_family)

    def _update_grid_width(self, root: JSONNode) -> None:
        for node in root:
            prefix_length = max((node.get_level() - 1) * 3 + 2, 0)
            name_length = len(node.get_name()) + 2
            if node.is_leaf() and node.get_value() is not None:
                name_length += len(node.get_value()) + 2
            self._grid_width = max(self._grid_width, prefix_length + name_length + 2)

    def _render_node(self, node: JSONNode, is_first: bool, is_last: bool, icon_family: IconFamily) -> None:
        result = ''
        # first layer
        if is_first:
            result += "┌─"
        elif is_last:
            result += "└─"
        elif node.get_level() == 1:
            result += "├─"
        else:
            result += "│ "
        # straight lines
        if node.get_level() > 2:
            if is_last:
                result += '─┴─' * (node.get_level() - 2)
            else:
                result += ' │ ' * (node.get_level() - 2)
        # header
        if is_last:
            result += '─┴─'
        elif node.get_level() > 1:
            result += ' ├─'
        # icon
        if node.is_leaf():
            result += icon_family.leaf_icon
        else:
            result += icon_family.composite_icon
        # name
        result += node.get_name()
        # value
        if node.is_leaf() and node.get_value() is not None:
            result += f': {node.get_value()}'
        # padding
        result = f'{result} '.ljust(self._grid_width - 2, '─')
        # last layer
        if is_first:
            result += '─┐'
        elif is_last:
            result += '─┘'
        else:
            result += '─┤'
        print(result)