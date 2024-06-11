import argparse
from .display import JSONNodeDrawer
from .node import JSONNodeFactory
from .exception import FJEException

def parse_args():
    parser = argparse.ArgumentParser(description='Funny JSON Explorer')
    parser.add_argument('-f', '--file', type=str, help='JSON file path')
    parser.add_argument('-s', '--style', type=str, help='style', default='tree')
    parser.add_argument('-i', '--icon-family', type=str, help='icon family', default='default')
    parser.add_argument('-c', '--config', type=str, help='icon family file')
    parser.add_argument('-v', '--verbose', action='store_true', help='print availavle icon families and styles', default=False)
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        drawer = JSONNodeDrawer()
        if args.config is not None:
            drawer.load_icon_family(args.config)
        if args.verbose:
            print(f'available icon families: {drawer.get_available_icon_families()}')
            print(f'available styles: {drawer.get_available_styles()}')
        else:
            if args.file is None:
                raise FJEException('请输入JSON文件路径')
            root = JSONNodeFactory(args.file).create()
            drawer.set_icon_family(args.icon_family)
            drawer.set_style(args.style)
            drawer.draw(root)
    except FJEException as e:
        print(f'Error: {e}')
    