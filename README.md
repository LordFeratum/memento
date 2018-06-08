# Memento
Software to create checkpoints and rollback for your data

# What is Memento
Memento is a software capable of create a checkpoint (many of them) and rollback to them. This checkpoints are associated to a specific data. You can only use Memento on python objects.

# What is not Memento
Memento cant generate a checkpoint for an entire context. For now at least.

# How to use
## As context manager
You can create a memento instance as a context manager.
``` python
from memento import Memento

class A:
  def __init__(self, a):
    self.v = a
  
  def inc(self, v=1):
    self.v += v
    
a = A(4)
a.inc()
with Memento(a) as m:
   a.inc()
   print(a.v)  # 6
   m()
   print(a.v)  # 5
```

## As a context manager with automatic rollback
``` python
a = A(4)
a.inc()
print(a.v)  # 5
with Memento(a, rollback_on_exc=True) as m:
  a.inc()
  print(a.v)  # 6
  a.inc("2")  # --> Raises an exception
  
print(a.v)  # 5
```

## As a context manager with error handling
``` python
def handler(exc, obj):
  print(exc)  # ValueError
  print(obj.v)  # 6

a = A(4)
a.inc()
print(a.v)  # 5
with Memento(a, exc_cb=handler, rollback_on_exc=True) as m:
  a.inc()
  print(a.v)  # 6
  a.inc("2")  # --> Raises an exception
  
print(a.v)  # 5
```

## As a normal instance
``` python
a = A(4)
a.inc()
print(a.v)  # 5
m = Memento(a)
a.inc()
print(a.v)  # 6
m()
print(a.v)  # 5
```

## How to change how Memento keep the state
You have to define two functions. One for copy the data, and another to recover the state.

``` python
class A:
  def __init__(self, v):
    self.v = v
  def inc(self, v=1):
    self.v += 1
  def copy(self):
    return self.v
  def restore(self, data):
    self.v = data
    
a = A(4)
m = Memento(a, copy_method=lambda x: x.copy(), recovery_method=lambda x, data: x.restore(data))
a.inc()
print(a.v)  # 5
m()
print(a.v)  # 4
```

