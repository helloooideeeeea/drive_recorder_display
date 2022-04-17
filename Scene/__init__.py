from abc import ABCMeta, abstractmethod


class Scene(metaclass=ABCMeta):

    @abstractmethod
    def loop(self):
        raise NotImplementedError()

    @abstractmethod
    def click_notify(self, position):
        raise NotImplementedError()

    @abstractmethod
    def before_finish(self):
        raise NotImplementedError()
