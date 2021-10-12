import numpy as np


def objective_function(x, y):
    """
    We are looking for this function minima
    """
    first_term = np.power(x, 2) + y - 11
    second_term = x + np.power(y, 2) - 7
    return np.power(first_term, 2) + np.power(second_term, 2)


class Particle:
    def __init__(self, inertia=0.5, social=2, cognitive=1):
        self.pos = np.random.uniform(low=-10, high=10, size=(1, 2))[0]
        self.vel = np.random.uniform(size=(1, 2))[0]
        self.pos_best = []
        self.err = -1
        self.err_best = -1
        # params
        self.inertia = inertia
        self.social = social
        self.cognitive = cognitive

    # evaluate current fitness
    def evaluate(self, objective_function):
        self.err = objective_function(self.pos[0], self.pos[1])
        # check to see if the current position is an individual best
        if self.err < self.err_best or self.err_best == -1:
            self.pos_best = self.pos
            self.err_best = self.err

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        w = (
            self.inertia
        )  # constant inertia weight (how much to weigh the previous velocity)
        c1 = self.cognitive  # cognative constant
        c2 = self.social  # social constant

        r1 = np.random.uniform()
        r2 = np.random.uniform()
        vel_cognitive = c1 * r1 * (self.pos_best - self.pos)
        vel_social = c2 * r2 * (pos_best_g - self.pos)
        self.vel = w * self.vel + vel_cognitive + vel_social

    # update the particle position based off new velocity updates
    def update_position(self):
        self.pos = self.pos + self.vel


class PSO:
    def __init__(self, objective_function, size, ngen):
        err_best = -1  # best error for group
        pos_best = []  # best position for group

        swarm = [Particle() for i in range(size)]

        # begin optimization loop
        i = 0
        while i < ngen:
            print(i, err_best)
            # cycle through particles in swarm and evaluate fitness
            for j in range(size):
                swarm[j].evaluate(objective_function)

                # determine if current particle is the best (globally)
                if swarm[j].err < err_best or err_best == -1:
                    pos_best = swarm[j].pos
                    err_best = swarm[j].err

            # cycle through swarm and update velocities and position
            for j in range(size):
                swarm[j].update_velocity(pos_best)
                swarm[j].update_position()
            i += 1

        # print final results
        print(f"FINAL: \n- Best solution: {pos_best}\n- Best error: {err_best}")


if __name__ == "__main__":
    swarm_size = 100
    ngen = 30
    PSO(objective_function, swarm_size, ngen)
