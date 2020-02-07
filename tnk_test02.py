from lark import Lark
from lark.indenter import Indenter

class PythonIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

kwargs = dict(rel_to=__file__, postlex=PythonIndenter(), start='file_input')

parser = Lark.open('tnk.lark',parser='lalr', **kwargs)


program = open("tnk_sample02.tnk", **{'encoding': 'iso-8859-1'}).read() +"\n"
tree = parser.parse(program)


print(tree)
print(tree.pretty())





class Variable:
    def __init__(self, key, taipu, value):
        self.key = key
        self.


class Environment():
    def __init__(self, parent_env):
        self._parent_env = parent_env
        self._dct = dict()

    def __contains__(self, key):
        return key in self._dct

    def get(self, key):
        value = self._dct.get(key, None)
        if not value:
            value = self._parent_env.get(key)
        return value

    def set(self, key, value):
        self._dct[key] = value


class Visitor():
    def program(self, tree, env):
        for sub_tree in tree.children:
            r = self._visit(sub_tree, env)
            if sub_tree.data == 'return_state':
                return r

    def _visit(self, tree, env):
        f = getattr(self, tree.data)
        return f(tree, env)

    def _declare_with_value(self, k, v, env):
        key = k.children[0].value
        value = self._visit(v, env)
        env.set(key, value)

    def declare_with_value_stmt(self, tree, env):
        for k,v in zip(tree.children[0].children, tree.children[1].children):
            self._declare_with_value(k, v, env)


    """
    def assign_stmt(self, tree, env):
        key = self._visit(tree.children[0], env)
        print(key)
        value = self._visit(tree.children[1], env)
        print(value)


    def muldiv_expr(self, tree, env):
        if tree.children[1]=="*":
            return self._visit(tree.children[0], env) * self._visit(tree.children[2], env)
        elif tree.children[1]=="/":
            return self._visit(tree.children[0], env) / self._visit(tree.children[2], env)


    def rekkyo(self, tree, env):
        return tuple(self._visit(tree.children[i], env) for i in range(len(tree.children)))

    def new_symbol(self, tree, env):
        key = tree.children[0].value
        if key in env:
            raise Exception("The symbol is already declared")
        return key
    """
    def symbol(self, tree, env):
        key = tree.children[0].value
        return env.get(key)

    def number(self, tree, env):
        return float(tree.children[0].value)


visitor = Visitor()
print(visitor.program(tree, Environment(None)))