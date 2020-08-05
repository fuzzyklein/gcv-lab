from fractions import Fraction
import math
import string

class Percentage(Fraction):
    def __init__(self, *args, **kwargs):
        Fraction.__init__(*args, **kwargs)
        self.templ_str = string.Template("{:.${precision}}")
        self._tolerance = 2

    def __repr__(self):
        return self.templ_str.substitute(precision=self.precision).format(self.value) + '%'

    def __str__(self):
        return self.__repr__()

    @property
    def precision(self):
        return math.ceil(math.log10(math.floor(self.value))) + self.tolerance

    @property
    def tolerance(self):
        """ Number of digits to display after the decimal point. """
        return self._tolerance

    @tolerance.setter
    def tolerance(self, n):
        self._tolerance = n

    @tolerance.deleter
    def tolerance(self):
        del self._tolerance

    @property
    def value(self):
        return self.numerator / self.denominator * 100
