from abc import ABC, abstractmethod


class Observer:
    # an abstract class of an observer, which is a user
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
    # class the implements the observable aspect of a user
    def __init__(self):
        self._observers = set()  # a set of all the followers of a user

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, post):
        # method that notifies all the follower of a user about a new post
        for u in self._observers:
            u.update(post)

    def notifylike(self, post, user):
        # method that notifies the user about a new like
        u = post.getUser()
        u.updatelike(post, user)

    def notifycomment(self, post, user, text):
        # method that notifies the user about a new comment
        u = post.getUser()
        u.updatecomment(post, user, text)

    def getSet(self):
        # method that returns a set of all the observers (followers) of the observable (user)
        return self._observers
