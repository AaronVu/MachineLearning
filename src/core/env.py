# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import tensorflow as tf


class Environment(object):

    def __init__(self):
        pass

    def reset(self):
        pass

    def step(self, action):
        """
        :param action:
        :return: observation，reward，done，info
        """
        pass

    def render(self, mode='human', close=False):
        pass

