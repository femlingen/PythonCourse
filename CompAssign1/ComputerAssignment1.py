import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from matplotlib.collections import LineCollection
from scipy.sparse import csgraph
import math
import time
from scipy.spatial import cKDTree

""" This is an assignment in course Object Oriented Programming in Python - DAT171 """
__author__ = "Lucas Jutvik & Frida Femling"

# --- Variable declaration ---

PIE = np.pi
file_name = ['SampleCoordinates.txt', 'HungaryCities.txt', 'GermanyCities.txt']
radius_list = np.array([0.08, 0.005, 0.0025])
country = 1
start_nodes = [0, 311, 1573]
end_nodes = [5, 702, 10584]
R = 1  # Calculing the mercant projection


# --- Task 1 --- create method to read a file and convert the latitude and longitude to degrees
# and return a Numpy array with X and Y coordinates

def read_coordinate_file(filename):

    """
    Read_coordinate_file
    :param filename takes a string of a filename as to open it
    :type filename str
    returns a list of coordinate pairs
    """

    long_lat_list = []
    with open(filename, 'r') as file:
        for line in file:
            long_lat_list.append([float(i) for i in (line.strip('{}\n').split(','))])
        x_y_cord = np.array(long_lat_list)
        x_y_cord[:, 1] *= R * PIE / 180
        x_y_cord[:, 0] = R * np.log(np.tan(PIE * (1 / 4 + x_y_cord[:, 0] / 360)))
            # Measuring distances on a Mercator projection isn’t very accurate, but will suffice for this task
        return np.flip(x_y_cord, axis=1)
        # line = file.readline()
        # while line:
        #     long_lat_list.append([float(i) for i in (line.strip('{}\n').split(','))])
        #     line = file.readline()
        # x_y_cord = np.array(long_lat_list)
        # x_y_cord[:, 1] *= R * PIE / 180
        # x_y_cord[:, 0] = R * np.log(np.tan(PIE * (1 / 4 + x_y_cord[:, 0] / 360)))
        # # Measuring distances on a Mercator projection isn’t very accurate, but will suffice for this task
        # return np.flip(x_y_cord, axis=1)


# --- Task 2, 5 & 8 --- Write the function  plot_points(coord_list)  which plots the data points read from the file
# using the function from task 1 to plot the points

def plot_points(coord_list, indices, path):
    """
    plot_points creates a plot with all cities and the paths in between, it also plots the cheapest path
    :param coord_list: a list of coordinate pairs
    :param indices: a list of indices of the connected cities
    :param path: the cheapest path (list of indices
    list of ints and floats
    """
    lc_list = coord_list[indices]

    line_segment = LineCollection(lc_list, linewidths=0.2)

    fig = plt.figure()
    plt.plot(coord_list[:, 0], coord_list[:, 1], 'dk', markersize=0.3)
    plt.plot(coord_list[path, 0], coord_list[path, 1], linewidth=0.5, color='red')
    ax = fig.gca()
    ax.add_collection(line_segment)
    plt.axis('equal')
    plt.show()


# --- Task 3 --- Create the function construct_graph_connections(coord_list, radius)
# that computes all the connections between all the points in  coord_list that are within the radius given.

def construct_graph_connections(coord_list, radius):
    """
    construct_graph_connections creates a list of connected cities and also the cost to drive between them
    :param coord_list: a list of coordinate pairs
    :param radius: a maximum radius
    :type
    All variables should be ints
    """
    index_list = []
    cost_list = []
    for i1, cord in enumerate(coord_list):
        for i2, cord2 in enumerate(coord_list[(i1 + 1)::], start=(i1 + 1)):
            dist = math.sqrt((cord[0] - cord2[0]) ** 2 + (cord[1] - cord2[1]) ** 2)
            if dist <= radius:
                index_list.append([i1, i2])
                cost_list.append(dist ** (9 / 10))
    new_index_list = np.array(index_list)

    return new_index_list, np.array(cost_list)


# --- Task 4 --- Create the function  construct_graph(indices, costs, N)
# that constructs a sparse graph. The graph should be represented as a compressed sparse row matrix
# The graph should be represented as a compressed sparse row matrix ( csr_matrix  in  scipy.sparse )

def construct_graph(indices, cost, n):
    """
    construct_graph creates a csr matrix
    :parameter
    indices: a list of all the connected cities
    cost: the cost to drive between connected cities
    N: The amount of cities in the country
    :return
    csr_matrix
    :type
    Indices and N should be ints
    cost can be int or float
    """
    csr_values = csr_matrix((cost, indices.T), shape=(n, n))
    # By translation of the indices we send them in with the right format and won't have to split them up
    return csr_values


# --- Task 7 --- One of the outputs from the cheapest path functions in SciPy is a “predecessor matrix”.
# The columns represent the predecessor when taking the cheapest path to the given column index.

def compute_path(predecessor_matrix, start_node, end_node):
    """
    compute_path finds the cheapest path given the pred_matrix
    :parameter
    predecessor_matrix: A predecessor matrix
    start_node: starting city
    end_node: end city
    :type
    All should be ints
    :return
    A nparray of the cities connected to the cheapest path
    """
    cities = [end_node]
    while cities[-1] != start_node:  # iterating from the last city to the start node to find the path
        cities.append(predecessor_matrix[cities[-1]])
    path = np.array(cities)
    return np.flip(path, axis=0)


# --- Task 10 --- Create the function  construct_ fast _graph_connections(coord_list, radius)
# that computes all the connections between all the points in  coord_list that are within the radius given.

def construct_fast_graph_connections(coord_list, radius):
    """
    construct_fast_graph_connections will create a list of connected cities and the cost driving between them
    :type radius: float
    :param coord_list: a list of coordinate pairs
    :param radius: the maximum radius
    :return list of connected cities
    :return cost of driving between them
    """
    c_l = coord_list
    coord_tree = cKDTree(c_l)
    all_neighbours = coord_tree.query_ball_point(c_l, radius)
    index_list = []
    cost_list = []
    for i1, neighbours in enumerate(all_neighbours):
        for i2 in neighbours:
            if i2 > i1:
                dist = math.sqrt((c_l[i1, 0] - c_l[i2, 0]) ** 2 + (c_l[i1, 1] - c_l[i2, 1]) ** 2)
                index_list.append([i1, i2])
                cost_list.append(dist ** (9 / 10))
    index_list = np.array(index_list)
    cost_list = np.array(cost_list)
    return index_list, cost_list


# Testing function Task 1
# including this time measurement to show how we did.
# Similar is done to each function and added as appendix to assignment hand in
time_list = []
start_time = time.time()
coordinates_list = read_coordinate_file(file_name[country])  # reads coordinates from file
end_time = time.time()
elapsed_time = end_time - start_time
time_list.append(elapsed_time)


# Testing function Task 3
connected, city_cost = construct_graph_connections(coordinates_list, radius_list[country])  # construct the
# connections between nodes

# Testing function Task 4
csr_matrice = construct_graph(connected, city_cost, len(coordinates_list))  # creating a csr matrice and putting the
# indices and cost in the matrice
# -- Task 6 ---

"""

Using Dijkstras algorithm:  

Arguments: Matrix - input csr matrix into Dijkstra 
           Indices of start node for specific country
           return_predecessors=True - only returns the predecessors if true
           directed=False finds the shortest path on undirected graph. Not point to point specified. 

Returns: Returns a list with the cost from each specific city with regards to start node
         Returns a predecessor matrix including of which cities to go through to get the cheapest path

"""

total_cost_list, predecessor = csgraph.dijkstra(
    csgraph=csr_matrice, indices=start_nodes[country], return_predecessors=True, directed=False)

path_cheapest = compute_path(predecessor, start_nodes[country], end_nodes[country])

total_cost = total_cost_list[end_nodes[country]]
plot_points(coordinates_list, connected, path_cheapest)

print('The cheapest route is the following: \n{}'.format(path_cheapest))
print('The total cost ammounts to: {}'.format(total_cost))