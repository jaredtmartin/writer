class A(object):
    def go(self):
        return "A"

class B(object):
    def go(self):
        return super(B,self).go()+"B"
        
class C(B):
    def go(self):
        return super(C,self).go()+"C"

class D(C): pass
d=D()
d.go()

Authentecated           user(hidden), title, description, screenshot
Admin

NonAuthenticated        email, name, title, description





non auth ['name', 'email', 'title', 'body']

normal user ['title', 'body']

admin ['title', 'body', 'status']
