
def assert_value(condition: bool, condition_as_string: str = '{unknown}'):
    if not condition:
        raise ValueError(f"Assertion failed: {condition_as_string}")


def assert_type(variable, types_, variable_name: str = '{unknown}'):
    if not isinstance(variable, types_):
        raise TypeError(f"Wrong type for variable {variable_name}\n    Given: {type(variable)}\n    Possible: {types_}")


class Book:
    """ Базовый класс книги. """
    def __init__(self, name: str, author: str):
        self.__name = name
        self.__author = author

    @property
    def name(self):
        return self.__name

    @property
    def author(self):
        return self.__author

    def __str__(self):
        return f"Книга {self.name}. Автор {self.author}"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, author={self.author!r})"


class PaperBook(Book):
    def __init__(self, name: str, author: str, pages: int):
        super().__init__(name, author)
        assert_type(pages, int)
        assert_value(pages > 0, "pages > 0")
        self.pages = pages

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, author={self.author!r}, pages={self.pages!r})"


class AudioBook(Book):
    def __init__(self, name: str, author: str, duration: float):
        super().__init__(name, author)
        assert_type(duration, float)
        assert_value(duration > 0, "duration > 0")
        self.duration = duration

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, author={self.author!r}, duration={self.duration!r})"

