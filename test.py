class A:
    def log(self, message):
        print(message)


class B(A):
    def foo(self):
        return "foo from B"


class C(A):
    def foo(self):
        return "foo from C"


class D(B, C):
    def bar(self):
        print(B.foo(self))
        print(C.foo(self))
        self.log("testtt")


d = D()
print(d.foo())
