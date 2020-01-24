from lark import Lark
from lark.indenter import Indenter


program = open('source01.tnk').read()
rule = open('grammer.txt').read()

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

parser = Lark(rule, start='program', parser='lalr', postlex=TreeIndenter())
tree = parser.parse(program)


print(tree)
print(tree.pretty())