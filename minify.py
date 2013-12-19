#!/usr/bin/env python3

# minify.py --- Minify well-formed HTML files containing CSS and Javascript.
# Copyright (C) 2013 kennytm
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import re

TAG_RE = re.compile(r'<[^>]+>')
END_TAG_RE = re.compile(r'</(?:script|style)>')
SPACE_RE = re.compile(r'(?<![\w$])\s|\s(?![\w$])|/\*(?:[^*]|\*[^/])*\*/')

def minify_css_or_js(text):
    return SPACE_RE.sub('', text)

def main(args):
    if len(args) < 1:
        sys.stderr.write('Usage: ./minify.py [input.html] > [output.html]\n')
        return

    with open(args[0], 'r') as f:
        text = f.read()

    next_index = 0
    while True:
        tag_m = TAG_RE.search(text, pos=next_index)
        if not tag_m:
            break

        tag = tag_m.group()

        sys.stdout.write(tag)
        next_index = tag_m.end()

        if tag in ('<script>', '<style>'):
            end_tag_m = END_TAG_RE.search(text, pos=next_index)
            if not end_tag_m:
                break

            content = text[next_index:end_tag_m.start()]
            sys.stdout.write(minify_css_or_js(content))
            sys.stdout.write(end_tag_m.group())
            next_index = end_tag_m.end()

if __name__ == '__main__':
    main(sys.argv[1:])

