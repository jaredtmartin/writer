class A(object):
  l=[1,2]
  def collect_l(self): 
    print "self.__class__.__bases__ = %s" % str(self.__class__.__bases__)
    l = []
    for superclass in self.__class__.__bases__:
      l.append(superclass.l)
    return l
  def collect_bases(self, classType):
    bases = [classType]
    for baseClassType in classType.__bases__:
        bases.append(self.collect_bases(baseClassType))
    return bases
  def get_bases(self):
    return self.collect_bases(self.__class__)
class B(A):
  l=[3,4]

class C(B):
  l=[5,6]
def get_bases(classType):
  bases = [classType]
  # recursive bases scan
  for baseClassType in classType.__bases__:
      bases.append(get_bases(baseClassType))
  return bases
o = C()
print "o.collect_l() = %s" % str(o.collect_l())

print "get_bases(o.__class__) = %s" % str(get_bases(o.__class__))
print "o.get_bases() = %s" % str(o.get_bases())