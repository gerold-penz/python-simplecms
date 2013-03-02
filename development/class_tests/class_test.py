# coding: utf-8


class A(object):

    class B(object):

        def __init__(self):
            self.a = A()

    def __init__(self):

        pass

    def make_b(self):
        self.b = self.B()


a = A()
a.make_b()
print a.b.a
a.b.a.make_b()
print a.b.a.b.a

