from matplotlib.pyplot import figure, plot, scatter

class Vector2(object):
    p = 2
    def __init__(self, x, y):
        self.x, self.y = x,y
    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x*other, self.y*other)
        elif isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
    def __truediv__(self, other):
        return Vector2(self.x/other, self.y/other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    def normalise(self):
        return (1/self.norm)*self
    def __str__(self):
        return("(" + str(self.x) + "," + str(self.y) + ")")
    def __iter__(self):
        for i in [self.x, self.y]:
            yield i
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    @property
    def perpendicular(self):
        return Vector2(-self.y, self.x)
    @property
    def norm(self):
        return (abs(self.x) ** Vector2.p + abs(self.y) ** Vector2.p) ** (1 / Vector2.p)


class Point2(Vector2):
    def plot(self):
        scatter(self.x, self.y)

    @classmethod
    def INFINITY(cls):
        return Point2(float('+inf'), float('+inf'))

class Matrix2(object):
    def __init__(self, v1: Vector2, v2: Vector2):
        self.v1 = v1
        self.v2 = v2
    def __add__(self, other):
        return Matrix2(self.v1+other.v1, self.v2+other.v2)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        return Matrix2(self.v1 - other.v1, self.v2 - other.v2)
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Matrix2(self.v1*other, self.v2*other)
        elif isinstance(other, Vector2):
            return self.v1*other.x + self.v2*other.y
        elif isinstance(other, Matrix2):
            return Matrix2(self*other.v1, self*other.v2)
    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Matrix2(self.v1/other, self.v2/other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __neg__(self):
        return Matrix2(-self.v1, -self.v2)
    @property
    def determinant(self):
        return self.v1.x*self.v2.y - self.v1.y*self.v2.x
    @property
    def traspose(self):
        return self*Matrix2(Vector2(0, 1), Vector2(1, 0))
    @property
    def inverse(self):
        return 1/self.determinant*Matrix2(Vector2(self.v2.y, -self.v1.y), Vector2(-self.v2.x, self.v1.x))


class Line(object):
    def __init__(self, v: Vector2, p: Vector2):
        self.v = v
        self.p = p

    def intersect(self, other):
        v1, n1 = self.v, self.p
        v2, n2 = other.v, other.p
        M, b = Matrix2(v1, -v2), n2 - n1
        M_1 = M.inverse
        l_d = M_1 * b

        return v1 * l_d.x + n1

    def __str__(self):
        return ("Line: v=" + str(self.v) + " p=" +str(self.p))

class Border(object):
    def __init__(self, p1: Vector2, p2: Vector2):
        self.p1, self.p2 = p1, p2
        self.separates = ()

    def plot(self):
        plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y])

    def does_limit(self, point: Point2):
        return point in self.separates

    def toLine(self):
        return Line(self.p1-self.p2, self.p1)

    def does_belong(self, point: Vector2):
        M = Matrix2(self.p1, self.p2)
        M_1 = M.inverse
        param = M_1*point
        return sum(param) == 1 and all(i >= 0 and i <= 1 for i in param)

    def split(self, point:Vector2):
        '''Assummes the point is in border'''
        return Border(self.p1, point), Border(self.p2, point)

    def __str__(self):
        return("Border: " + str(self.p1) + " <-> " + str(self.p2))

