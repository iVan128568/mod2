from __future__ import annotations
from typing import Generator
import doctest


def assert_value(condition: bool, condition_as_string: str = '{unknown}'):
    if not condition:
        raise ValueError(f"Assertion failed: {condition_as_string}")


def assert_type(variable, types_, variable_name: str = '{unknown}'):
    if not isinstance(variable, types_):
        raise TypeError(f"Wrong type for variable {variable_name}\n    Given: {type(variable)}\n    Possible: {types_}")


class BitNumber:
    """
    Class to use a bit representation of some number

    Attributes:
        __number: A value stores the number
            [User shouldn't access it. All the work with it will be using class methods]
        __len: Stores amount of bits in number (ignoring leading zeros)
            [User shouldn't access it. It will be only exported by __len__ method]
    """
    def __init__(self, number: (int, BitNumber) = 0) -> None:
        """
        Initialization

        :param number: The number to represent (must be >= 0)

        Examples:
        >>> bn = BitNumber(175)
        """
        if isinstance(number, BitNumber):
            self.__number = number.__number
            self.__len = number.__len
            return
        assert_type(number, int, 'number')
        assert_value(number >= 0, "number >= 0")
        self.__number = number
        self.__len = len(bin(self.__number)[2:])

    def __xor__(self, other: (int, BitNumber)) -> BitNumber:
        """
        Xor operation

        :param other: Second operand
        :return: Result of xor

        Examples:
        >>> bn = BitNumber(175)
        >>> print(bn ^ 3)
        10101100
        """
        other = BitNumber(other)
        return BitNumber(self.__number ^ other.__number)

    def __rshift__(self, num: int) -> BitNumber:
        """
        Bit shift right operation

        :param num: Shifts amount
        :return: Result of bit shift

        Examples:
        >>> bn = BitNumber(175)
        >>> print(bn >> 3)
        10101
        """
        assert_type(num, int, 'num')
        return BitNumber(self.__number >> num)

    def __lshift__(self, num: int) -> BitNumber:
        """
        Bit shift left operation

        :param num: Shifts amount
        :return: Result of bit shift

        Examples:
        >>> bn = BitNumber(175)
        >>> print(bn << 3)
        10101111000
        """
        assert_type(num, int, 'num')
        return BitNumber(self.__number << num)

    def __len__(self) -> int:
        """
        Returns length

        :return: Length

        Examples:
        >>> bn = BitNumber(175)
        >>> len(bn)
        8
        """
        return self.__len

    def __getitem__(self, index: int) -> int:
        """
        Returns one bit of number by its index

        :param index: Index of bit in number (it must be 0 <= index < len(self))
        :return: Bit on position INDEX

        Examples:
        >>> bn = BitNumber(175)
        >>> bn[3]
        1
        """
        assert_type(index, int, 'index')
        assert_value(0 <= index < len(self), "0 <= index < len(self)")
        return (self.__number >> index) % 2

    def __iter__(self) -> Generator[int, None, None]:
        """
        Performs iteration over all bits in number

        :return: Generator that yields all bits in number sequentially

        Examples:
        >>> bn = BitNumber(175)
        >>> for bit in bn:
        ...     print(bit, end='|')
        1|1|1|1|0|1|0|1|
        """
        for i in range(len(self)):
            yield self[i]

    def __int__(self) -> int:
        """
        Casts BitNumber to int type

        :return: BitNumber cast to int type

        Examples:
        >>> bn = BitNumber(175)
        >>> print(int(bn))
        175
        """
        return self.__number

    def bin(self) -> str:
        """
        Formats number to binary format

        :return: String representing number in binary format

        Examples:
        >>> bn = BitNumber(175)
        >>> print(bn.bin())
        0b10101111
        """
        return bin(self.__number)

    def __hex__(self) -> str:
        """
        Formats number to hexedecimal format

        :return: String representing number in hexedecimal format

        Examples:
        >>> bn = BitNumber(175)
        >>> print(bn.__hex__())
        af
        """
        return hex(self.__number)[2:]

    def __str__(self) -> str:
        """
        Formats number to string format

        :return: String representing number

        Examples:
        >>> bn = BitNumber(175)
        >>> print(bn)
        10101111
        """
        return bin(self.__number)[2:]

    def __repr__(self) -> str:
        """
        Creates string to represent this object

        :return: String representing this object

        Examples:
        >>> bn_list = [BitNumber(175), BitNumber(10), BitNumber(15)]
        >>> print(bn_list)
        [BitNumber(0b10101111), BitNumber(0b1010), BitNumber(0b1111)]
        """
        return f"{self.__class__.__name__}({bin(self.__number)})"


class GFNumber:
    """
    Number in Galois field

    Attributes:
        _number: A value stores the bit number
            [User shouldn't access it. All the work with it will be using class methods]
        _len: Stores the length of the number
            [User shouldn't access it. It will be only exported by __len__ method]
    """
    def __init__(self, number: (int, BitNumber, GFNumber) = 0) -> None:
        """
        Initialization

        :param number: Initial value of number (must be >= 0)

        Examples:
        >>> gfn = GFNumber(175)
        """
        if isinstance(number, GFNumber):
            self._number = BitNumber(number._number)
            self._len = len(self._number)
            return

        assert_type(number, (int, BitNumber), 'number')
        if isinstance(number, int):
            assert_value(number >= 0, "number >= 0")
            number = BitNumber(number)
        if isinstance(number, BitNumber):
            number = BitNumber(number)
        self._number = number
        self._len = len(number)

    def __add__(self, other: (int, BitNumber, GFNumber)) -> GFNumber:
        """
        Addition operation

        :param other: Second operand
        :return: Result of addition

        Examples:
        >>> gfn = GFNumber(175)
        >>> print(gfn + 3)
        x7 + x5 + x3 + x2
        """
        other = GFNumber(other)
        return GFNumber(self._number ^ other._number)

    def __mul__(self, other: (int, BitNumber, GFNumber)) -> GFNumber:
        """
        Multiplication operation

        :param other: Second operand
        :return: Result of multiplication

        Examples:
        >>> gfn = GFNumber(175)
        >>> print(gfn * 3)
        x8 + x7 + x6 + x5 + x4 + 1
        """
        other = GFNumber(other)

        result_number = BitNumber(0)
        for index, bit in enumerate(other._number):
            if bit:
                result_number ^= (self._number << index)

        return GFNumber(result_number)

    __rmul__ = __mul__

    def __len__(self) -> int:
        """
        Returns length

        :return: Length

        Examples:
        >>> gfn = GFNumber(175)
        >>> len(gfn)
        8
        """
        return self._len

    def __getitem__(self, index) -> int:
        """
        Returns one bit of number by its index

        :param index: Index of bit in number
        :return: Bit on position INDEX

        Examples:
        >>> gfn = GFNumber(175)
        >>> gfn[3]
        1
        """
        return self._number[index]

    def __int__(self) -> int:
        """
        Casts GFNumber to int type

        :return: GFNumber cast to int type

        Examples:
        >>> gfn = GFNumber(175)
        >>> print(int(gfn))
        175
        """
        return int(self._number)

    def bin(self) -> str:
        """
        Formats number to binary format

        :return: String representing number in binary format

        Examples:
        >>> gfn = GFNumber(175)
        >>> print(gfn.bin())
        0b10101111
        """
        return self._number.bin()

    def __hex__(self, prefix: str = '0x'):
        """
        Formats number to hexedecimal format

        :param prefix: String to put before actual value
        :return: String representing number in hexedecimal format

        Examples:
        >>> gfn = GFNumber(175)
        >>> print(gfn.__hex__())
        0xaf
        """
        return prefix + self._number.__hex__()

    def __str__(self) -> str:
        """
        Formats number to string format

        :return: String representing number

        Examples:
        >>> gfn = GFNumber(175)
        >>> print(gfn)
        x7 + x5 + x3 + x2 + x + 1
        """
        str_ = ''
        print_num = 0
        for i, bit in enumerate(self._number):
            power = i
            if bit:
                if print_num:
                    str_ = ' + ' + str_
                print_num += 1
                if power:
                    str_ = f'x{"" if power == 1 else power}' + str_
                else:
                    str_ = '1' + str_
        return str_

    def __repr__(self) -> str:
        """
        Creates string to represent this object

        :return: String representing this object

        Examples:
        >>> gfn_list = [GFNumber(175), GFNumber(10), GFNumber(15)]
        >>> print(gfn_list)
        [GFNumber(0b10101111), GFNumber(0b1010), GFNumber(0b1111)]
        """
        return f"{self.__class__.__name__}({self._number.bin()})"


class GF8Number(GFNumber):
    """
    Number in Galois field of order p^8
    """
    MAX_BITS = 8
    SHRINK_MODULO = BitNumber(0b100011011)

    def __init__(self, number: (int, BitNumber, GFNumber, GF8Number) = 0, assert_shrunk: bool = False) -> None:
        """
        Initialization

        :param number: Initial value of number

        Examples:
        >>> gf8n = GF8Number(175)
        """
        super().__init__(number)
        shrunk = self.__shrink()
        if assert_shrunk:
            assert_value(shrunk is False, 'shrunk == False')

    def __shrink(self) -> bool:
        """
        Shrinks number to fit in this size field

        :return: If transformation was required to fit
        """
        if len(self) <= self.MAX_BITS:
            return False
        for i in range(len(self) - 1, self.MAX_BITS - 1, -1):
            if self[i]:
                self._number ^= self.SHRINK_MODULO << (i - self.MAX_BITS)
        self._len = len(self._number)
        return True

    def __mul__(self, other: (int, BitNumber, GFNumber, GF8Number)) -> GF8Number:
        """
        Multiplication operation asures that result will fit in this size field
        (Unlike multiplication for galois field of any order this function makes sure
        result is also will be an element of galois field of order p^8)

        :param other: Second operand
        :return: Result of multiplication

        Examples:
        >>> gf8n = GF8Number(175)
        >>> print(gf8n * 3)
        x7 + x6 + x5 + x3 + x
        """
        other = GF8Number(other, assert_shrunk=True)
        result = GF8Number(super().__mul__(other))
        result.__shrink()
        return result

    def __hex__(self, prefix: str = '0x'):
        """
        Formats number to hexedecimal format

        :param prefix: String to put before actual value
        :return: String representing number in hexedecimal format

        Examples:
        >>> gf8n = GF8Number(175)
        >>> print(gf8n.__hex__())
        0xaf
        """
        hex_str = self._number.__hex__()
        len_ = self.MAX_BITS // 4
        return prefix + hex_str.rjust(len_, '0')


if __name__ == "__main__":
    doctest.testmod()