from lark import Lark


program = open('source01.tnk').read()
rule = open('grammer.txt').read()


parser = Lark(rule, start='program', parser='lalr')
tree = parser.parse(program)


print(tree)