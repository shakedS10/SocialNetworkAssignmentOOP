from abc import ABC, abstractmethod


class Observer:
    @abstractmethod
    def update(self, post):
        pass

    @abstractmethod
    def updatelike(self, post, user):
        pass

    @abstractmethod
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
        for u in self._observers:
            u.update(post)

    def notifylike(self, post, user):
        u = post.getUser()
        u.updatelike(post, user)

    def notifycomment(self, post, user, text):
        u = post.getUser()
        u.updatecomment(post, user, text)
    def getSet(self):
        return self._observers