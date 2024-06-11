# 设计文档

## 类图说明与项目结构

模块说明：

1. exception: 定义了一个异常类，用于捕获所有预期的异常
2. main: 读取命令行参数，调用 JSONNodeFactory 工厂读取 json 文件并创建 JSONNode，然后将参数传入 JSONNodeDrawer，让其读取 IconFamily 文件，渲染出对应的风格。
3. node: 定义了项目使用的可视化数据结构，同时包含一个读取 json 文件创建该数据结构的简单工厂
4. icon: 存储处理 icon 相关的数据
5. display: 存储风格渲染相关的类
   1. display: 定义了策略接口 DisplayStrategy
   2. `__init__`: 定义了一个建造者 JSONNodeDrawer ，负责获取对应的策略和 icon_family 并完成渲染
   3. tree_style: 定义了一个树形风格的策略
   4. rectangle_style: 定义了一个矩形风格的策略

类图：

![](./design.jpg)

## 使用的设计模式

1. 建造者： JSONNodeDrawer 是建造者接口。在重构前他负责生产 StyledJSONNode，但由于这个对象在之前就只有渲染功能，不如让 JSONNodeDrawer 直接调用。尽管 JSONNodeDrawer 已经不再生产对象，其模式依然与建造者类似，通过设置不同样式来决定渲染方式。
2. 组合模式： JSONNode、JSONLeaf、JSONComposite 是组合模式的实现，分别对应 component、leaf、composite。
3. 简单工厂： JSONNodeFactory 是简单工厂，他根据文件名读取 json 并创建 JSONNode 产品。
4. 迭代器模式：JSONNode 定义了 `__iter__` 方法，子类通过 python 的生成器模式实现了迭代器功能，可以方便地遍历节点。
5. 策略模式： DisplayStrategy 接口定义了渲染策略，其子类 tree_style 和 rectangle_style 实现了不同的渲染方式。