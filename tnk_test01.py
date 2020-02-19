from lark import Lark
from lark.indenter import Indenter

class MyIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

kwargs = dict(rel_to=__file__, postlex=MyIndenter(), start='file_input')

parser = Lark.open('tnk.lark',parser='lalr', **kwargs)


program = open("tnk_sample01.tnk", **{'encoding': 'iso-8859-1'}).read() +"\n"
tree = parser.parse(program)


print(tree.pretty())