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


program = open("tnk_sample04.tnk", **{'encoding': 'iso-8859-1'}).read() +"\n"
tree = parser.parse(program)


print(tree.pretty())




class TNKNameError(Exception):
    pass

class Variable:
    def __init__(self, typ, value):
        self.typ = typ
        self.value = value

    def __str__(self):
        typnam = str(self.typ)[8:-2]
        return f"{typnam}({self.value})"

    def __repr__(self):
        typnam = str(self.typ)[8:-2]
        return f"{typnam}({self.value})"

    def __add__(self,other):
        value = self.value + other.value
        typ = type(value)
        return Variable(typ, value)

    def __sub__(self,other):
        value = self.value - other.value
        typ = type(value)
        return Variable(typ, value)

    def __mul__(self,other):
        value = self.value * other.value
        typ = type(value)
        return Variable(typ, value)

    def __truediv__(self,other):
        value = self.value / other.value
        typ = type(value)
        return Variable(typ, value)




# Bool, Int, Float, Complex, Seq[...], Tensor[...]





class Scope:
    def __init__(self, parent_scope=None):
        self._parent_scope = parent_scope or NullScope()
        self._dct = dict()

    def __str__(self):
        return f"Scope({self._dct})"

    def defined_in_this_scope(self, key):
        return key in self._dct

    def defined_anywhere(self, key):
        if key in self._dct:
            return True
        return self._parent_scope.defined_anywhere(key)

    def get(self, key):
        value = self._dct.get(key, None)
        if not value:
            value = self._parent_scope.get(key)
        return value

    def assign(self, key, value):
        if self.defined_in_this_scope(key):
            self._dct[key] = value
            return
        self._parent_scope.assign(key, value)

    def declare(self, key, value):
        if self.defined_in_this_scope(key):
            raise TNKNameError(f"Name {key} is already defined in this scope.")
        self._dct[key] = value


class NullScope(Scope):
    def __init__(self):
        pass

    def defined_anywhere(self, key):
        return False

    def get(self, key):
        raise TNKNameError(f"Name {key} is not defined.")

    def assign(self, key, value):
        raise TNKNameError(f"Name {key} is not defined.")

    def declare(self, key, value):
        raise TNKNameError(f"Name {key} is already defined in this scope.")



class Visitor():
    def program(self, tree):
        scope = Scope()
        for sub_tree in tree.children:
            self._visit(sub_tree, scope)
        print(scope)

    def _visit(self, tree, env):
        f = getattr(self, tree.data)
        return f(tree, env)

    def _declare_with_value(self, k, v, env):
        key = k.children[0].value
        value = self._visit(v, env)
        env.declare(key, value)

    def declare_with_value_stmt(self, tree, env):
        for k,v in zip(tree.children[0].children, tree.children[1].children):
            self._declare_with_value(k, v, env)

    def symbol(self, tree, env):
        key = tree.children[0].value
        return env.get(key)

    def dec_number(self, tree, env):
        v = tree.children[0].value
        return Variable(int, int(v))

    def float_number(self, tree, env):
        v = tree.children[0].value
        return Variable(float, float(v))

    def complex_number(self, tree, env):
        v = tree.children[0].value
        return Variable(complex, complex(v))

    def addsub_expr(self, tree, env):
        left = self._visit(tree.children[0], env)
        op = tree.children[1]
        right = self._visit(tree.children[2], env)
        if op == "+":
            return left + right
        elif op == "-":
            return left - right

    def muldiv_expr(self, tree, env):
        left = self._visit(tree.children[0], env)
        op = tree.children[1]
        right = self._visit(tree.children[2], env)
        if op == "*":
            return left * right
        elif op == "/":
            return left / right



visitor = Visitor()
print(visitor.program(tree))



"""
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

    ""
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
    ""


    def symbol(self, tree, env):
        key = tree.children[0].value
        return env.get(key)

    def number(self, tree, env):
        return float(tree.children[0].value)
"""