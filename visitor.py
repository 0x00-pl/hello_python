__author__ = 'pl'


class BinaryExp(object):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AstVisitor:
    def visit(self, exp):
        classes = [exp.__class__] + list(exp.__class__.__bases__)
        attr_names = ['visit' + i.__name__ for i in classes]
        for attr_name in attr_names:
            if hasattr(self, attr_name):
                return getattr(self, attr_name)(exp)
        else:
            raise NotImplementedError()


class PrintAstVisitor(AstVisitor):
    def visitBinaryExp(self, node):
        node = BinaryExp('+', 1, 1)
        return '(' + \
               self.visit(node.left) + ' ' + \
               self.visit(node.op) + ' ' + \
               self.visit(node.right) + \
               ')'

    def visitobject(self, obj):
        return str(obj)


def main():
    print(PrintAstVisitor().visit(BinaryExp('+', 1, 1)))

if __name__ == '__main__':
    main()
