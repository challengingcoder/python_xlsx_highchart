import argparse
import os
import sys

if sys.version_info[0] != 3:
    print("Python 3 required!")
    sys.exit(1)

os.sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    parser = argparse.ArgumentParser(description='')
    cmd_list = (
        'app',
        'test'
    )

    parser.add_argument('cmd', choices=cmd_list, nargs='?', default='app')

    args = parser.parse_args()
    cmd = args.cmd

    if cmd == 'app':
        from pptxbuilder.app import main
        main()

    if cmd == 'test':
        from pptxbuilder.tests import do_tests
        do_tests()


if __name__ == '__main__':
    main()