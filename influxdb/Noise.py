#! /usr/bin/env python
#-*- coding:utf-8 -*-
import math
import random

V = 30
Q = 1
class noisy():
    def noise(timestamp):
        hour = timestamp//3600
        if hour <= 5:
            Q = 50
        elif hour <= 7:
            Q = 800 * (hour - 4)
        elif hour <= 9:
            Q = 2000
        elif hour <= 12:
            Q = 2000 - 800 * (hour - 10)
        elif hour <= 15:
            Q = 800
        elif hour <= 17:
            Q = 800 * (hour - 14)
        elif hour <= 19:
            Q = 2000
        elif hour <= 21:
            Q = 2000 - 1000 * (hour - 19)
        else:
            Q = 50
            Q = Q + random.randint(-20, 20)
        if(Q <= 0):
            Q = 1
        noisy = 55.7+0.12*(V-50)-8.06*math.log10(V) + 9.97*math.log10(Q)
        noisy = round(noisy, 2)
        return noisy