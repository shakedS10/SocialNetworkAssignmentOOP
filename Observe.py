from abc import ABC, abstractmethod
class Observer:
    @abstractmethod
    def update(self, post):
        pass
    def updatelike(self, post, user):
        pass
    def updatecomment(self, post, user, text):
        pass

class Observable(ABC):
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, post):
        for observer in self._observers:
            observer.update(post)
    def notifylike(self, post, user):
        for observer in self._observers:
            observer.updatelike(post, user)
    def notifycomment(self, post, user, text):
        for observer in self._observers:
            observer.updatecomment(post, user, text)