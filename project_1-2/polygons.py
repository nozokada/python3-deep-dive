from math import cos, sin, pi


def lazy(fn):
    my_cache = None

    def _cache_wrapper(*args, **kwargs):
        nonlocal my_cache
        if not my_cache:
            my_cache = fn(*args, **kwargs)
        return my_cache
    return _cache_wrapper

lazy_property = lambda fn: property(lazy(fn))


class Polygon:

    def __init__(self, edges: int, circ_r: int):
        if edges < 3 or circ_r < 1:
            raise Exception
        self.edges = edges
        self.circ_r = circ_r

    @property
    def vertices(self):
        return self.edges

    @property
    @lazy
    def apothem(self):
        apothem = self.circ_r * cos(pi / self.edges)
        return apothem

    @lazy_property
    def edge_length(self):
        edge_length = 2 * self.circ_r * sin(pi / self.edges)
        return edge_length

    @lazy_property
    def interior_angle(self):
        interior_angle = (self.edges - 2) * (180 / self.edges)
        return interior_angle

    @lazy_property
    def perimeter(self):
        perimeter = self.edges * self.edge_length
        return perimeter

    @lazy_property
    def area(self):
        area = .5 * self.edges * self.edge_length * self.apothem
        return area

    @lazy_property
    def ratio(self):
        ratio = self.area / self.perimeter
        return ratio

    def __repr__(self):
        return f'Polygon: edges:{self.edges} circumradius:{self.circ_r} area:{self.area}'

    def __eq__(self, other):
        if isinstance(other, Polygon):
            raise Exception
        return self.vertices == other.vertices and self.circ_r == other.circ_r

    def __gt__(self, other):
        if isinstance(other, Polygon):
            raise Exception
        return self.vertices > other.vertices


class PolygonsIterator:

    def __init__(self, polygons):
        self.polygons = polygons
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.polygons[self._i]
            self._i += 1
        except IndexError:
            raise StopIteration

        return result


class Polygons:

    min_vertices = 3

    def __init__(self, max_vertices, circ_r):
        if max_vertices < self.min_vertices:
            raise Exception
        self.max_vertices = max_vertices
        self.circ_r = circ_r

    def __getitem__(self, item):
        if self.max_vertices - item < self.min_vertices:
            raise IndexError
        return Polygons._pol(item, self.max_vertices, self.circ_r)

    def __len__(self):
        return self.max_vertices - self.min_vertices + 1

    @property
    def max_efficiency_polygon(self):
        mep = self[0]
        mep_ratio = mep.area / mep.perimeter
        for pol in self:
            ratio = pol.area / pol.perimeter
            if ratio > mep_ratio:
                mep = pol
                mep_ratio = ratio
        return mep

    @staticmethod
    def _pol(index, max_vertices, circ_r):
        return Polygon(edges=max_vertices-index, circ_r=circ_r)


pol = Polygon(edges=3, circ_r=1)

# polygons = PolygonsIterator(Polygons(max_vertices=10, circ_r=1))
# for polygon in polygons:
#     print(f'{polygon} perimeter:{polygon.perimeter} ratio:{polygon.ratio}')
# print(f'Maximum efficiency polygon:\n{polygons.polygons.max_efficiency_polygon}')
