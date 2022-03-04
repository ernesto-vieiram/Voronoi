import random
import matplotlib.pyplot as plt
from vector import Vector2, Matrix2

def get_points_set(N_POINTS, N_CLASSES):
    POINTS = []
    CLASSES = []
    i = 0
    random.seed(100)
    while i < N_POINTS:
        POINTS.append(Vector2(random.random(), random.random()))
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
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.gca().set_aspect('equal', adjustable='box')
    return figure

def graph_points(POINTS, figure):
    plt.figure(figure)
    plt.scatter([tuple(p)[0] for p in POINTS], [tuple(p)[1] for p in POINTS], c=CLASSES, s=20)



def graph_closest_line (points, closests, figure ,k = 1):
    plt.figure(figure)
    for i in range(N_POINTS):
        point = tuple(points[i])
        closest = tuple(points[closests[i][1]])
        plt.plot([point[0], closest[0]], [point[1], closest[1]])

def graph_mediatrices(points, closests, figure, l = 2):
    for i in range(N_POINTS):
        point = points[i]
        closest1, closest2 = points[closests[i][1]], points[closests[i][2]]
        graph_mediatriz(point, closest1, figure, l)

def graph_mediatriz(p1: Vector2, p2: Vector2, figure ,l = 1):
    #l is line length
    plt.figure(figure)
    dif = p1-p2
    perp = dif.perpendicular.normalise()
    middle = (p1+p2)/2

    p_1, p_2 = perp*l + middle, -perp*l + middle
    p_1, p_2 = tuple(p_1), tuple(p_2)

    plt.plot([p_1[0], p_2[0]], [p_1[1], p_2[1]])

def create_mediatrix(p1: Vector2, p2: Vector2):
    dif = p1 - p2
    perp = dif.perpendicular.normalise()
    middle = (p1 + p2) / 2
    return (perp, middle)

def calculate_intersection(r1, r2):
    v1, m1 = r1[0], r1[1]
    v2, m2 = r2[0], r2[1]
    M, b = Matrix2(v1,-v2), m2-m1
    M_1 = M.inverse
    l_d = M_1*b

    intersection1 = v1 * l_d.x + m1
    intersection2 = v2 * l_d.y + m2
    return intersection1


def create_intersection_points(points: [Vector2]):
    mediatrices = []
    for i in range(N_POINTS-1):
        for j in range(i+1, N_POINTS):
            mediatrices.append(create_mediatrix(points[i], points[j]))
    intersecciones = []
    for i in range(len(mediatrices)-1):
        for j in range(i+1, len(mediatrices)):
            intersecciones.append(calculate_intersection(mediatrices[i], mediatrices[j]))
    return intersecciones

def delete_redundant(points, intersecciones, clases, k = 1):
    final = []
    for interseccion in intersecciones:
        closests = get_closest(interseccion, points)
        #len(closests) > k and
        if len(closests) > k:
            final.append(interseccion)
    return final

def get_closest(point: Vector2, points):
    tolerance = 0.000001
    close_points = []
    best = float('+inf')
    for target_i in range(len(points)):
        target = points[target_i]
        dif = point-target
        distancia = dif.norm
        if best-distancia > tolerance :
            close_points = []
            close_points.append(target_i)
            best = distancia
        elif abs(best-distancia) < tolerance:
            close_points.append(target_i)
    return close_points

def decide_class(closest, clases, k):
    if len(closest) < k:
        return None
    best = 0
    classes_vote = [0 for _ in range(N_CLASSES)]
    for point in closest:
        clase = clases[point]
        classes_vote[clase] += 1
    print(classes_vote)
    return best



N_POINTS = 2
N_CLASSES = N_POINTS
k = 1
Vector2.p = 2

POINTS, CLASSES = get_points_set(N_POINTS, N_CLASSES)
DISTANCES = get_distances(POINTS)
CLOSESTS = get_closests(DISTANCES)

fig = create_frame(N_POINTS, N_CLASSES, k)
graph_points(POINTS, fig)

#graph_closest_line(POINTS, CLOSESTS, figure)
#graph_mediatrices(POINTS, CLOSESTS, figure, 5)
#INTERSECCIONES = create_intersection_points(POINTS)
#plt.scatter([tuple(p)[0] for p in INTERSECCIONES], [tuple(p)[1] for p in INTERSECCIONES], s=7)
#FINAL = delete_redundant(POINTS, INTERSECCIONES, CLASSES)
#plt.scatter([tuple(p)[0] for p in FINAL], [tuple(p)[1] for p in FINAL], s=7)

plt.show()

