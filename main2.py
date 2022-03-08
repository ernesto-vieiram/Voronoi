import random
import matplotlib.pyplot as plt
from vector import Vector2, Matrix2, Line, Border

def get_points_set(N_POINTS, N_CLASSES):
    POINTS = []
    CLASSES = []
    i = 0
    random.seed(100)
    while i < N_POINTS:
        POINTS.append(Vector2(2*random.random()-1, 2*random.random()-1))
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

def get_region_borders(point: Vector2, borders):
    ret = []
    does = None
    for border in borders:
        #POINT TO BEGIN CYCLE FROM BORDER
        does =  border.does_limit(point)
        if does != None: break
    if does == None: return []
    #START POINT: DOES & BORDER
    next = border.get_next(does)
    next_p = border.get_next_point(does)
    ret.append(border)
    while next != border:
        ret.append(next)
        prev = next_p
        next_p = next.get_next_point(prev)
        next = next.get_next(prev)
    return ret

def create_mediatrix(p1: Vector2, p2: Vector2):
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

init_point = POINTS[0]
b_d = Border(Vector2(-1, -1), Vector2(1,-1))
b_r = Border(Vector2(1, -1), Vector2(1,1))
b_u = Border(Vector2(1, 1), Vector2(-1,1))
b_l = Border(Vector2(-1, 1), Vector2(-1,-1))
b_d.set_next((1,-1), b_l)
b_l.set_next((-1, -1), b_u)
b_u.set_next((-1, 1), b_r)
b_r.set_next((1,1), b_d)
b_d.separates = {(-1, -1): Vector2.INFINITY(), (1,-1): init_point}
b_l.separates = {(-1, 1): Vector2.INFINITY(), (-1,-1): init_point}
b_u.separates = {(1, 1): Vector2.INFINITY(), (-1,1): init_point}
b_r.separates = {(1, -1): Vector2.INFINITY(), (1,1): init_point}
BORDERS = [b_d, b_r, b_l, b_u]

plt.figure(fig)
#VORONOI
for point_i in range(1,N_POINTS):
    point = POINTS[point_i]
    point.plot()
    #GET POINT OF REGION
    belongs = POINTS[CLOSESTS[point_i][1]]
    #GET BORDERS OF REGION
    region_border = get_region_borders(belongs, BORDERS)
    #CALCULATE BISECTOR point - belongs
    bisector = create_mediatrix(point, belongs)
    INTERSECTIONS = []
    print(belongs, [str(i) for i in region_border])
    #UPDATE BORDERS
    for border in region_border:
        #TODO: DETECT IF AN INTERSECTION IS WITH A FRAME OR OTHER
        #CALCULATE INTERSECTION OF BISECTOR WITH BORDERS
        intersection = calculate_intersection(border.toLine(), bisector)
        #CHECK IF INTERSECTION POINT IS IN BORDER LIMITS
        if border.does_belong(intersection):
            #IF IT EXISTS; ADD INTERSECTION, SPLIT THE BORDER INTO TWO BORDERS
            INTERSECTIONS.append(intersection)
            b1, b2 = border.split(intersection)
            #TODO: INICIALIZAR NEXTS de b1 y b2
            v1 = b1.p1-intersection
            v2 = b2.p2-intersection
            v = belongs-intersection
            for p in border.separates:
                if border.separates[p] != point: other = border.separates[p]
            if v1*v > 0:
                #Border b1 restringe belongs
                b1.separates = (belongs, other)
                #Border b2 restringe point
                b2.separates = (point, other)
            else:
                #Border b1 restringe point
                b1.separates = (point, other)
                #Border b2 restringe belongs
                b2.separates = (belongs, other)
            BORDERS.remove(border)
            BORDERS.append(b1)
            BORDERS.append(b2)
        #TODO: update border if it does not limit point anynmore -> change to
    print(len(INTERSECTIONS))
    print(INTERSECTIONS[0])
    b_v = INTERSECTIONS[0]-INTERSECTIONS[1]


graph_points(POINTS, fig)
graph_borders(BORDERS, fig)

plt.show()