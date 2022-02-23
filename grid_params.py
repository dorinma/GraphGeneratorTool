class Grid:
    xs, ys, zs = 0, 0, 0
    blocks = 0  # Number of blocks on the grid
    axes_movement = 0   # Movement is allowed in how many axes
    movement_cost = 0   # 0 for const weight, 1 for random
    cost_min, cost_max = -1, -1

    def __init__(self):
        pass

    def set_values(self, xs, ys, zs, blocks, axes_movement, movement_cost, cost_min, cost_max):
        self.xs, self.ys, self.zs, blocks, self.axes_movement, self.movement_cost = xs, ys, zs, blocks, axes_movement, \
                                                                                    movement_cost
        if movement_cost == 1:
            self.cost_min, self.cost_max = cost_min, cost_max
