"""
设计模式：
1. 建造者模式：创建渲染JSONNode的各个部件然后渲染。不过他并不是用来创建对象的，而是直接用来完成任务。
"""
from ..exception import FJEException
from ..icon import IconFamily
from ..node import JSONNode
from typing import Dict
from .display import DisplayStrategy
from .tree_style import DisplayTreeStyle
from .rectangle_style import DisplayRectangleStyle
import os
import json

class JSONNodeDrawer:

    def __init__(self):
        self._icon_families = {
            'default': IconFamily(' ', ' '),
            'poker-face-icon-family': IconFamily('\u2666', '\u2660')
        }
        self._display_strategy: Dict[str, DisplayStrategy] = {
            'tree': DisplayTreeStyle(),
            'rect': DisplayRectangleStyle()
        }
        self._selected_icon_family = self._icon_families['default']
        self._selected_style = self._display_strategy['tree']

    def draw(self, root: JSONNode) -> None:
        self._selected_style.display(root, self._selected_icon_family)

    def set_icon_family(self, icon_family: str) -> None:
        try:
            self._selected_icon_family = self._icon_families[icon_family]
        except KeyError:
            raise FJEException(f'找不到图标集：{icon_family}')
    
    def set_style(self, style: str) -> None:
        try:
            self._selected_style = self._display_strategy[style]
        except KeyError:
            raise FJEException(f'找不到样式：{style}')
    
    def load_icon_family(self, filepath):
        if os.path.isfile(filepath) == False:
            raise FJEException(f'找不到图标集文件：{filepath}')
        with open(filepath, 'r', encoding='utf-8') as f:
            icon_family_dict = json.load(f)
        try:
            for name, icon_family in icon_family_dict.items():
                self._icon_families[name] = IconFamily(icon_family['composite'], icon_family['leaf'])
        except KeyError:
            raise FJEException(f'图标集文件格式错误：{filepath}')

    def get_available_styles(self):
        return list(self._display_strategy.keys())
    
    def get_available_icon_families(self):
        return list(self._icon_families.keys())