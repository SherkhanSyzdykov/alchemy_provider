"""
Implements cls or instance decorator
https://stackoverflow.com/questions/28237955/same-name-for-classmethod-and-instancemethod#:~:text=Class%20and%20instance%20methods%20live,will%20win%20in%20that%20case.&text=This%20is%20explicitly%20documented%3A,instance%20(such%20as%20C().
"""


class cls_or_ins(classmethod):
    def __get__(self, instance, type_):
        descr_get = super().__get__ \
            if instance is None else self.__func__.__get__
        return descr_get(instance, type_)
