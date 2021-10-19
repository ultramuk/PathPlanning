import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class Obstacle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def plot(self, color='k'):
        theta = np.linspace(0, np.pi*2, num=30)
        x = self.x + self.r * np.cos(theta)
        y = self.y + self.r * np.sin(theta)

        plt.plot(x, y, color=color)

    def is_inside(self, x, y):
        dist = np.hypot(x - self.x, y - self.y)
        if dist <= self.r:
            return True
        else:
            return False

def SampleFree(space, goal):
    min_x, max_x, min_y, max_y = space
    if np.random.rand() > 0.04:
        rand_x = np.random.uniform(min_x, max_x)
        rand_y = np.random.uniform(min_y, max_y)
    else:
        rand_x = goal[0]
        rand_y = goal[1]

    node_rand = {"x": rand_x, "y": rand_y, "cost": 1e9}
    return node_rand

def Nearest(G, node_rand):
    min_dist = 1e9
    for v in G.nodes:
        node = G.node[v]
        dist = np.hypot(node_rand["x"] - node["x"], node_rand["y"] - node["y"])
        if dist < min_dist:
            node_nearest = node
            node_nearest_id = v
            min_dist = dist
    return node_nearest, node_nearest_id

def Steer(node_nearest, node_rand):
    # step = 3.0
    step = np.random.uniform(1.0, 5.0)

    dx = node_rand["x"] - node_nearest["x"]
    dy = node_rand["y"] - node_nearest["y"]
    magnitude = np.hypot(dx, dy)

    # node_new = node_nearest + dir * step
    x_new = node_nearest["x"] + dx/magnitude * step
    y_new = node_nearest["y"] + dy/magnitude * step

    return {"x": x_new, "y": y_new, "cost": 1e9}

def ObstacleFree(node_nearest, node_new, obstacles):
    step = 0.2
    dx = node_new["x"] - node_nearest["x"]
    dy = node_new["y"] - node_nearest["y"]
    magnitude = np.hypot(dx, dy)

    # u = 0.0 --> node_nearest
    # u = magnitude --> node_new
    u = 0.0
    us = []
    while u < magnitude:
        us.append(u)
        u += step
    us.append(magnitude)

    for u in us:
        x_new = node_nearest["x"] + dx/magnitude * u
        y_new = node_nearest["y"] + dy/magnitude * u
        for obstacle in obstacles:
            collide = obstacle.is_inside(x_new, y_new)
            if collide:
                return False
    return True

def IsGoal(node_new, goal):
    dist = np.hypot(node_new["x"] - goal[0], node_new["y"] - goal[1])
    if dist < 2.0:
        return True
    else:
        return False

def DistanceToGoal(node, goal):
    dist = np.hypot(node["x"] - goal[0], node["y"] - goal[1])

def Near(G, node_new, radius):
    near_node_ids = []
    for v in G.nodes:
        node = G.node[v]
        dist = np.hypot(node_new["x"] - node["x"], node_new["y"] - node["y"])
        if dist < radius:
            near_node_ids.append(v)
    return near_node_ids

def LineCost(node_from, node_to):
    dx = node_to['x'] - node_from['x']
    dy = node_to['y'] - node_from['y']
    return np.hypot(dx, dy)


if __name__ == '__main__':
    ## environment setup
    np.random.seed(100)
    min_x, max_x = -20, 20
    min_y, max_y = -20, 20

    space = [min_x, max_x, min_y, max_y]

    start = np.random.uniform(low=-20, high=-5, size=2)
    goal = np.random.uniform(low=5, high=20, size=2)

    obstacles = []
    for i in range(25):
        x = np.random.uniform(low=min_x, high=max_x, size=1)
        y = np.random.uniform(low=min_y, high=max_y, size=1)
        r = np.random.uniform(low=1.0, high=5.0)
        obstacle = Obstacle(x, y, r)

        if not obstacle.is_inside(start[0], start[1]) and not obstacle.is_inside(goal[0], goal[1]):
            obstacles.append(obstacle)

    ## configuration
    gamma = 10.0
    eta = 10.0

    ## algorithm
    G = nx.DiGraph()
    G.add_nodes_from([
        (-1, {"x": start[0], "y": start[1], "cost": 0})
    ])

    max_iterations = 150
    goal_node_id = None
    min_goal_node_cost = 1e9
    for i in range(max_iterations):
        node_rand = SampleFree(space, goal)
        node_nearest, node_nearest_id = Nearest(G, node_rand)
        node_new = Steer(node_nearest, node_rand)
        if ObstacleFree(node_nearest, node_new, obstacles):
            card_v = len(list(G.nodes))
            radius = 4.0
            nodes_near_id = Near(G, node_new, radius)
            G.add_nodes_from([
                (i, node_new)
            ])

            node_min_id = node_nearest_id
            cost_min = G.node[node_nearest_id]["cost"] + LineCost(node_nearest, node_new)
            # Connect along a minimum-cost path
            for node_near_id in nodes_near_id:
                node_near = G.node[node_near_id]
                cost_near = node_near["cost"] + LineCost(node_near, node_new)
                if ObstacleFree(node_near, node_new, obstacles) and cost_near < cost_min:
                    node_min = node_near
                    node_min_id = node_near_id
                    cost_min = cost_near

            G.add_edge(node_min_id, i)
            G.node[i]["cost"] = cost_min
            node_new["cost"] = cost_min

            # Rewire the tree
            # (Your code here!)

            if IsGoal(node_new, goal):
                goal_node_cost = node_new["cost"]
                if goal_node_cost < min_goal_node_cost:
                    min_goal_node_cost = goal_node_cost
                    goal_node_id = i

    if goal_node_id is None:
        print(" [!] Cannot find path")
    else:
        path = nx.shortest_path(G, source=-1, target=goal_node_id)

    ## visualize
    for obs in obstacles:
        obs.plot()

    plt.plot(start[0], start[1], 'ro', ms=8)
    plt.plot(goal[0], goal[1], 'rx', ms=10)
    for v in G.nodes:
        plt.plot(G.node[v]["x"], G.node[v]["y"], 'b.')
        plt.text(G.node[v]["x"], G.node[v]["y"], v)

    for e in G.edges:
        # e = [v_from, v_to]
        v_from = G.node[e[0]]
        v_to = G.node[e[1]]

        plt.plot([v_from["x"], v_to["x"]], [v_from["y"], v_to["y"]], 'b-')

    if goal_node_id is not None:
        path_x = []
        path_y = []
        for v in path:
            path_x.append(G.node[v]["x"])
            path_y.append(G.node[v]["y"])
        plt.plot(path_x, path_y, 'r-')

    plt.axis("equal")
    plt.show()
