#!/usr/bin/env python

import pickle

selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)

output = pickle.Pickler(data.pkl)

# Pickle the list using the highest protocol available.
output.dump(selfref_list)

