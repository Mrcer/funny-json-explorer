# Funny JSON Explorer

Funny JSON Explorer (FJE)，是一个JSON文件可视化的命令行界面小工具

## 安装

本项目基于 python 编写，最低支持版本为 3.8，不依赖任何外部库，在项目根目录下运行以下命令安装：

```shell
pip install -e .
```

卸载方式如下：

```shell
pip uninstall fje
```

## 使用

在使用 pip 安装 fje 后，你可以直接在命令行中使用 `fje` 命令打开 Funny JSON Explorer：

```shell
fje path/to/your/json/file
```

## 开发

## 测试

测试文件组织在 test 目录下，使用 unittest 进行测试：

```shell
# 在项目根目录下运行测试
python -m unittest test
```