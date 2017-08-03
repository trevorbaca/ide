#! /usr/bin/env python
import pathlib


for path in pathlib.Path('.').rglob('*.py'):
    with path.open() as file_pointer:
        lines = []
        for line in file_pointer.readlines():
            print(line)
            if line == '# -*- coding: utf-8 -*-\n':
                pass
            else:
                lines.append(line)
    string = ''.join(lines)
    with path.open('w') as file_pointer:
        file_pointer.write(string)
