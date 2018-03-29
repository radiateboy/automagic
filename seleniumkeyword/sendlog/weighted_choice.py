# -*- coding: utf-8 -*-
__author__ = 'Ray'

"""
通过概率产生随机值
mail：tsbc@vip.qq.com
2016-05-05
"""

import random
from collections import Counter

def weighted_choice_sub(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            # print w
            return i

weights = [0.03, 0.04, 0.05, 0.07, 0.1, 0.2, 0.5, 0.01]

# weighted_choice_sub(weights)

# count =Counter()
#
# for x in xrange(10000):
#     index = weighted_choice_sub(weights)
#     count[index] += 1
#
# count_sum = sum(count.values())
#
# for key, value in count.iteritems():
#     print float(value)/count_sum