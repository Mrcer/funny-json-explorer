"""
用于封装JSON数据结构的节点类
功能：
1. 从文件中获得JSON数据并解析为JSONNode对象
2. 对 Style 类提供接口，用于获取节点的信息
3. 实现遍历节点的功能
设计模式：
1. 组合模式：JSONNode 类是 JSONComposite 和 JSONLeaf 类是 JSONNode 类的子类，实现了组合模式。
2. 简单工厂模式：JSONNodeFactory 类是 JSONNode 的简单工厂类，用于从文件中读取JSON数据并解析为JSONNode对象。
"""
from abc import ABC, abstractmethod
from typing import List, Callable, Union
import json
import os
from .exception import FJEException
from typing import Generator

class JSONNode(ABC):

    def __init__(self, name: str, level: int):
        self._name = name
        self._level = level

    @abstractmethod
    def is_leaf(self) -> bool:
        pass

    def is_root(self) -> bool:
        return self._level == 0

    def get_name(self) -> str:
        return self._name
    
    def get_level(self) -> int:
        return self._level
    
    """
    按深度优先遍历节点"""
    @abstractmethod
    def __iter__(self) -> Generator['JSONNode', None, None]:
        pass
    
class JSONComposite(JSONNode):

    def __init__(self, name: str, level: int):
        super().__init__(name, level)
        self._children: List[JSONNode] = []

    def is_leaf(self) -> bool:
        return False

    def add_child(self, child: JSONNode):
        self._children.append(child)
    
    def get_children(self) -> List[JSONNode]:
        return self._children

    def __iter__(self) -> Generator[JSONNode, None, None]:
        yield self
        for child in self._children:
            yield from iter(child)
    
class JSONLeaf(JSONNode):

    def __init__(self, name: str, level: int, value: Union[str, None]):
        super().__init__(name, level)
        self._value = value

    def is_leaf(self) -> bool:
        return True

    def get_value(self) -> Union[str, None]:
        return self._value
    
    def __iter__(self) -> Generator[JSONNode, None, None]:
        yield self

"""
从文件中读取JSON数据并解析为JSONNode对象"""
class JSONNodeFactory:

    def __init__(self, filepath: str):
        if os.path.isfile(filepath) == False:
            raise FJEException(f'文件{filepath}不存在')
        with open(filepath, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
        if not isinstance(self.json_data, (dict, list)):
            raise FJEException(f'JSON根节点必须是字典或列表')
    
    def create(self) -> JSONNode:
        return self._create('', 0, self.json_data)

    def _create(self, name: str, level: int, obj) -> JSONNode:
        if isinstance(obj, list):
            return self._create_composite_from_list(name, level, obj)
        elif isinstance(obj, dict):
            return self._create_composite_from_dict(name, level, obj)
        else:
            return self._create_leaf(name, level, obj)

    def _create_composite_from_list(self, name: str, level: int, obj) -> JSONComposite:
        composite = JSONComposite(name, level)
        for idx, item in enumerate(obj):
            child = self._create(f'Array[{idx}]', level + 1, item)
            composite.add_child(child)
        return composite

    def _create_composite_from_dict(self, name: str, level: int, obj) -> JSONComposite:
        composite = JSONComposite(name, level)
        for key, value in obj.items():
            child = self._create(key, level + 1, value)
            composite.add_child(child)
        return composite
    
    def _create_leaf(self, name: str, level: int, obj) -> JSONLeaf:
        if obj is None:
            return JSONLeaf(name, level, None)
        else:
            return JSONLeaf(name, level, str(obj))