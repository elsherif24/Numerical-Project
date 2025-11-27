import math
from decimal import Decimal


class _Config:
    SIG_FIGS: int = 4  # default value


def set_sig_figs(sig: int):
    _Config.SIG_FIGS = sig


def get_sig_figs() -> int:
    return _Config.SIG_FIGS


def round_sig(x: Decimal, sig: int) -> Decimal:
    if x.is_zero():
        return Decimal("0")
    exp = x.adjusted() - sig + 1
    return x.quantize(Decimal(f"1e{exp}"))


class D:
    def __init__(self, value):
        self.val = round_sig(Decimal(str(value)), _Config.SIG_FIGS)

    def _apply(self, other, op):
        if isinstance(other, D):
            other = other.val
        result = op(self.val, Decimal(str(other)))
        return D(result)

    def __add__(self, other):
        return self._apply(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self._apply(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self._apply(other, lambda a, b: a * b)

    def __truediv__(self, other):
        return self._apply(other, lambda a, b: a / b)

    def __pow__(self, other):
        return self._apply(other, lambda a, b: a ** b)

    def __mod__(self, other):
        return self._apply(other, lambda a, b: a % b)

    def __floordiv__(self, other):
        return self._apply(other, lambda a, b: a // b)

    def __radd__(self, other):
        if other == 0:
            return self
        return self._apply(other, lambda a, b: b + a)

    def __rsub__(self, other):
        return self._apply(other, lambda a, b: b - a)

    def __rmul__(self, other):
        return self._apply(other, lambda a, b: b * a)

    def __rtruediv__(self, other):
        return self._apply(other, lambda a, b: b / a)

    def __rpow__(self, other):
        return self._apply(other, lambda a, b: b ** a)

    def __rmod__(self, other):
        return self._apply(other, lambda a, b: b % a)

    def __rfloordiv__(self, other):
        return self._apply(other, lambda a, b: b // a)

    def __neg__(self):
        return D(-self.val)

    def __pos__(self):
        return D(+self.val)

    def __abs__(self):
        return D(abs(self.val))

    def __eq__(self, other):
        if isinstance(other, D):
            return self.val == other.val
        return self.val == Decimal(str(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, D):
            return self.val < other.val
        return self.val < Decimal(str(other))

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, D):
            return self.val > other.val
        return self.val > Decimal(str(other))

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def sqrt(self):
        return D(self.val.sqrt())

    def exp(self):
        return D(self.val.exp())

    def ln(self):
        return D(self.val.ln())

    def log10(self):
        return D(self.val.log10())

    def log(self, base=None):
        if base is None:
            return self.ln()
        base_val = base.val if isinstance(base, D) else Decimal(str(base))
        return D(self.val.ln() / Decimal(str(base_val)).ln())

    def floor(self):
        return D(int(self.val))

    def ceil(self):
        return D(math.ceil(float(self.val)))

    def round(self, n=0):
        return D(round(float(self.val), n))

    def isNearZero(self):
        return abs(self.val) < Decimal("1e-6")

    def __float__(self):
        return float(self.val)

    def __int__(self):
        return int(self.val)

    def __bool__(self):
        return bool(self.val)

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return str(self.val)

    def __format__(self, format_spec):
        return format(str(self.val), format_spec)

    @classmethod
    def zero(cls):
        return cls(Decimal("0"))

    @classmethod
    def one(cls):
        return cls(Decimal("1"))

    @classmethod
    def zeros(cls, n):
        return [cls.zero() for _ in range(n)]

    @staticmethod
    def from_vector(vec):
        return [D(val) for val in vec]

    @staticmethod
    def from_matrix(mat):
        if hasattr(mat, "shape"):
            n_rows, n_cols = mat.shape
            return [[D(mat[i][j]) for j in range(n_cols)] for i in range(n_rows)]
        else:
            return [[D(val) for val in row] for row in mat]
