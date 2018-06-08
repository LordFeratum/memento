import queue


def recovery(obj, _copy):
    obj.__dict__.clear()
    obj.__dict__.update(_copy)


def copy(obj):
    from copy import deepcopy
    return deepcopy(obj.__dict__)


def memento(obj, copy_method=copy, recovery_method=recovery):
    _copy = copy_method(obj)

    def recover():
        recovery_method(obj, _copy)

    return recover


class Memento:
    def __init__(self, obj, copy_method=copy, recovery_method=recovery,
                 exc_cb=None, rollback_on_exc=True):
        self.obj = obj
        self._copy_method = copy_method
        self._recovery_method = recovery_method
        self.checkpoints = queue.LifoQueue()
        self.rollback_on_exc = rollback_on_exc
        self.exc_cb = exc_cb

        self.checkpoint()

    def _get_memento(self):
        return memento(self.obj,
                       copy_method=self._copy_method,
                       recovery_method=self._recovery_method)

    def checkpoint(self):
        self.checkpoints.put(self._get_memento())

    def rollback(self):
        while not self.checkpoints.empty():
            self()

    def __call__(self):
        if not self.checkpoints.empty():
            self.checkpoints.get()()

    def __enter__(self):
        return self

    def __exit__(self, exc_class, exc, tb):
        if exc is not None:
            if self.exc_cb is not None:
                if self.exc_cb.__code__.co_argcount == 1:
                    self.exc_cb(exc)
                elif self.exc_cb.__code__.co_argcount == 2:
                    self.exc_cb(exc, self.obj)

                if self.rollback_on_exc:
                    self.rollback()

                return True

            elif self.rollback_on_exc:
                self.rollback()

            return False

        return True
