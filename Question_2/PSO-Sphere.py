# Created by Huzefa

import SwarmPackagePy
import numpy as np
from SwarmPackagePy import testFunctions as tf
from SwarmPackagePy import animation, animation3D

# configure swarm-particle-optimization

result = []

for x in range(15):

	spo = SwarmPackagePy.pso(50, tf.sphere_function, -10, 10, 2, 15, w=0.5, c1=1, c2=1) # define dimensions and iteration

	#print(spo.get_Gbest())

	result.append(spo.get_Gbest())

	best_agent = result[x]
	min =  tf.ackley_function(best_agent)
	for agent in result:
		current_value = tf.ackley_function(agent)
		if min > current_value:
			min = current_value
			best_agent = agent
			print(min,',', best_agent)
