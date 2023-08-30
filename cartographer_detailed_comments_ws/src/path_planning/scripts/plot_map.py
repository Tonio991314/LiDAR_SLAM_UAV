#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys
import numpy as np

class Plotting:
    def __init__(self, data): 
        self.width, self.height = data.info.width, data.info.height
        self.boundary  = self.boundary(self.width, self.height)
        self.obstacles = self.obstacles(data, self.width)

    def boundary(self, width, height):
        boundary = [
            [0, 0, 1, height],
            [0, height, width, 1],
            [1, 0, width, 1],
            [width, 1, 1, height]
        ]
        return boundary
    
    def obstacles(self, data, width):
        obstacles = []
        indices = np.where(np.array(data.data) > 50)[0]
        Ox = indices % width
        Oy = (indices - Ox) // width

        # for i in range(len(Ox)):
        #     obstacles.append((Ox[i], Oy[i], 0.1))
        obstacles = np.vstack((Ox, Oy, np.full_like(Ox, 0.1, dtype=np.float64))).T.tolist()
        obstacles = list(map(tuple, obstacles))
        # convert to tuple


        return obstacles


    def plot_map(self):
        fig, ax = plt.subplots()

        for (ox, oy, w, h) in self.boundary:    
            ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )
        
        for (ox, oy, r) in self.obstacles:
            ax.add_patch(
                patches.Circle(
                    (ox, oy), r,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        plt.title("test")
        plt.axis("equal")
        plt.show()
    