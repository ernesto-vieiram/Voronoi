import random
import matplotlib.pyplot as plt
from vector import Vector2, Matrix2, Line, Border, Point2

def get_points_set(N_POINTS, N_CLASSES):
    POINTS = []
    CLASSES = []
    i = 0
    random.seed(100)
    while i < N_POINTS:
        POINTS.append(Point2(2*random.random()-1, 2*random.random()-1))
        CLASSES.append(random.randint(0, N_CLASSES - 1))
        i += 1
    return POINTS, CLASSES

def get_distances(points):
    DISTANCES = [[0 for _ in range(N_POINTS)] for _ in range(N_POINTS)]
    for i in range(N_POINTS):
        for j in range(i, N_POINTS):
            dif = points[i] - points[j]
            distancia = dif.norm
            DISTANCES[i][j] = distancia
            DISTANCES[j][i] = distancia
    return DISTANCES

def get_closests(distances, k = 1):
    CLOSEST = []
    for i in range(N_POINTS):
        indexes = range(N_POINTS)
        distance_arr = distances[i]
        CLOSEST.append([x for _, x in sorted(zip(distance_arr, indexes))])
    return CLOSEST

def create_frame(N_POINTS, N_CLASSES, k):
    figure = plt.figure()
    plt.title(str(N_POINTS) + " points. " + str(N_CLASSES) + " classes." + " k=" + str(k) + ". p=" + str(Vector2.p))
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    plt.gca().set_aspect('equal', adjustable='box')
    return figure

def graph_points(POINTS, figure):
    plt.figure(figure)
    plt.scatter([tuple(p)[0] for p in POINTS], [tuple(p)[1] for p in POINTS], c=CLASSES, s=20)

def graph_borders(BORDERS, figure):
    plt.figure(figure)
    for border in BORDERS: border.plot()

def get_region_borders(point: Point2, borders):
    ret = []
    for border in borders:
        assert isinstance(border, Border)
        if border.does_limit(point): ret.append(border)
    return ret

def create_mediatrix(p1: Point2, p2: Point2):
    dif = p1 - p2
    perp = dif.perpendicular.normalise()
    middle = (p1 + p2) / 2
    return Line(perp, middle)

def calculate_intersection(r1: Line, r2: Line):
    v1, m1 = r1.v, r1.p
    v2, m2 = r2.v, r2.p
    M, b = Matrix2(v1,-v2), m2-m1
    M_1 = M.inverse
    l_d = M_1*b

    intersection1 = v1 * l_d.x + m1
    return intersection1

######### VORONOI EXEC MAIN ##############
#Model Parameters
N_POINTS = 2
N_CLASSES = N_POINTS
k = 1
Vector2.p = 2

#Map initialisation
POINTS, CLASSES = get_points_set(N_POINTS, N_CLASSES)
DISTANCES = get_distances(POINTS)
CLOSESTS = get_closests(DISTANCES)
fig = create_frame(N_POINTS, N_CLASSES, k)
BORDERS = [
    Border(Point2(-1, -1), Point2(1,-1)),
    Border(Point2(1, -1), Point2(1,1)),
    Border(Point2(1, 1), Point2(-1,1)),
    Border(Point2(-1, 1), Point2(-1,-1))
]
init_point = POINTS[0]
for border in BORDERS:
    border.separates = (Point2.INFINITY(), init_point)

plt.figure(fig)
#VORONOI
for point_i in range(1,2):
    point = POINTS[point_i]
    point.plot()
    #GET POINT OF REGION
    belongs = POINTS[CLOSESTS[point_i][1]]
    #GET BORDERS OF REGION
    region_border = get_region_borders(belongs, BORDERS)
    #CALCULATE BISECTOR point - belongs
    bisector = create_mediatrix(point, belongs)
    #UPDATE BORDERS
    for border in region_border:
        #TODO: DETECT IF AN INTERSECTION IS WITH A FRAME OR OTHER
        #CALCULATE INTERSECTION OF BISECTOR WITH BORDERS
        intersection = calculate_intersection(border.toLine(), bisector)
        #CHECK IF INTERSECTION POINT IS IN BORDER LIMITS
        if border.does_belong(intersection):
            #IF IT EXISTS; SPLIT THE BORDER INTO TWO BORDERS
            b1, b2 = border.split(intersection)
            #TODO: UPDATE THE separates attribute OF b1 & b2
            # uno pertenece a belongs y otro
            v1 = b1.p1-intersection
            v2 = b2.p2-intersection
            v = belongs-intersection
            if v1*v > 0:
                #Border p1 restringe belongs
                #Border p2 restringe point
            else:
                #Border p1 restringe point
                #Border p2 restringe belongs



graph_points(POINTS, fig)
graph_borders(BORDERS, fig)

plt.show()