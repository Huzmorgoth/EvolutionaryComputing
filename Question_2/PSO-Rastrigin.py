# Created By Huzefa Shaikh

import sys
import random
import math
import numpy as np

'''dimension''' 
dim = 2
perfRes = []
#Particle-count-in-Swarm
particle_no = 15

# Bounds-on-positions-velocities
v_max = 20
v_min = -20
p_min = -32
p_max = 32

# updates_no
cmax = 1000

# amt-of-dampen-velocity-on-updates
dampener = 1
dampen_rate = 1

# Leaving original variables distinct
orig_dampen_rate = dampen_rate
orig_dampener = dampener

# Function-to-optimize (minimize)
def F(x):
  global dim
  D = dim
  summation = 0
  # D-dimensional Rastrigin Function
  
  i = 0
  summation = D*10
  while i < D:
    summation += x[i]**2 - 10 * math.cos(2 * math.pi * x[i])
    i = i + 1
  return summation

# main-function-construction-of-swarm-optimization

def main():

  
  for x in range(15):
    global cmax, dampener, dampen_rate, dim
    
    #running-multiple-iterations-with-while-loop
    dampen_rate = orig_dampen_rate
    dampener = orig_dampener
    # Construct the swarm
    swarm = []
    i = 0
    while i < particle_no:
      swarm.append(Particle())
      i = i + 1
          
    # Init-best-position-velocity-error
    best_pos = []
    worst_pos = []
    all_pos = []
    AvgX = 0
    AvgXc = []
    best_velocity = []
    best_err = -1
    worst_err = -1
    nerr = []
    # Run-updates-swarm-and-output-best-position/error
    i = 0
    while i <= cmax:
      # Iterate-swarm-and-evaluation-of-swarm-positions-on-the-function
      j = 0
      while j < len(swarm):
        err = swarm[j].Evaluate()
        #nerr.append(err)
        # If-particle-perform-better
        # Save-particle-position-velocity-error
        if err < best_err or best_err == -1:
          best_pos = []
          best_velocity = []
          k = 0
          while k < dim:
            best_pos.append(swarm[j].pos[len(swarm[j].pos)-1][k])
            
            best_velocity.append(swarm[j].velocity[len(swarm[j].velocity)-1][k])
            k = k + 1
          best_err = err
        j = j + 1
      
      # Update-swarm-based-on-new-positions
      j = 0
      while j < len(swarm):
        swarm[j].UpdateVelocity(best_pos)
        swarm[j].UpdatePosition()
        j = j + 1

      dampener = dampener * dampen_rate # Dampen the velocity
      i = i + 1

    # Output-stats

    #print 'performance of 15 run'
    perfRes.append(best_err)

    #print 'Run: ', x
    #print '\nBest-performance: ', best_err,' ---BEST-Positions: ', best_pos
    print best_err, best_pos
     
    #print '\nworst-performance: ', worst_err,' ---WORST-Positions: ', worst_pos
    
    
  # the below attributes are instances of each particle:

  # minimization

  '''
  err: current position's error
  best_pos: location of particle seen lowest error
  best_err: lowest error
  pos: particle seen location list(past positions are recyclable)
  velocity: The list of particle velocities
  '''
  nRess = np.array(perfRes)
  print '\nOver all best performance: ', min(perfRes)
  print '\nOver all worst performance: ', max(perfRes)
  print '\nAverage performance: ', np.mean(nRess)
  print '\n'
  
  return

class Particle:
  def __init__(self):
    global dim
    # this function sets up each particle
    # we can initialize the position and velocity of the particles
    # using the InitPosition() and InitVelocity() functions
    self.err = 0 
    self.best_pos = []
    self.best_err = -1 # this is set to -1 so we update after the first step
    self.pos = []
    self.velocity = []

    # Since we are operating in a potentially multi-dimensional space
    # we have to run through each of the positions, initializing the
    # positions and velocities for each dimension
    temp_pos = []
    temp_velocity = []
    j = 0
    while j < dim:
      temp_pos.append(self.InitPosition())
      temp_velocity.append(self.InitVelocity())
      self.best_pos.append(0) # initialize the best position array
      j = j + 1
    self.pos.append(temp_pos)
    self.velocity.append(temp_velocity)

  # Evaluate the performance of each particle
  # The current position of the particle is the last
  # array in the position array.
  def Evaluate(self):
    global dim
    # The F function that we are trying to minimize
    self.err = F(self.pos[len(self.pos)-1])
    if self.best_err == -1 or self.err < self.best_err:
      self.first_update = False
      self.best_err = self.err
      self.best_pos = []
      j = 0
      while j < dim:
        self.best_pos.append(self.pos[len(self.pos)-1][j])
        j = j + 1
    return self.err
  # Initialize the position of the particle between -30 and 30
  # for each dimension
  def InitPosition(self):
    temp = 30*random.random()
    if random.random() > 0.5:
      temp = -1 * temp
    if temp > p_max:
      return p_max
    elif temp < p_min:
      return p_min
    return temp

  # Initialize the velocity of the particle between 1 and -1
  # for each dimension
  def InitVelocity(self):
    if random.random() > 0.5:
      return random.random()
    return -1*random.random()

  # A function that is used to randomize the cognitive term
  def RandomizeCognitive(self):
    return random.random()

  # A function that is used to randomize the social term
  def RandomizeSocial(self):
    return random.random()

  # A function that is used to update the velocity
  # of the particle the particle's past and the global best position seen
  def UpdateVelocity(self, global_best_pos):
    global v_max, dampener, dim
    # w is a control parameter that tells the particle
    # how much to discount the previous velocity
    w = 1
    # c1 is a control parameter that tells the particle
    # how much to weight its own previous positions
    c1 = 2
    # c2 is a control parameter that tells the particle
    # how much to weight the swarms best best position
    c2 = 2
    # r1 and r2 are random numbers that weight the
    # cognitive and social terms
    r1 = self.RandomizeCognitive()
    r2 = self.RandomizeSocial()

    t = len(self.velocity)

    # Construct the new velocity for the particle
    new_velocity_arr = []
    j = 0
    while j < dim:
      # Apply the control parameters to the particle's previous velocity
      # in the direction that we are working on
      v_term = dampener*w*self.velocity[t-1][j]

      # Create the cognitive and social terms
      own_term = c1 * r1 * (self.best_pos[j] - self.pos[t-1][j])
      social_term = c2 * r2 * (global_best_pos[j] - self.pos[t-1][j])
      # Add the velocities together to make the new velocity
      new_velocity = v_term + own_term + social_term

      # If the velocity is larger than the max velocity, decrease it
      # If the velocity is smaller than the min velocity, increase it
      if new_velocity > v_max:
        new_velocity = v_max
      elif new_velocity < v_min:
        new_velocity = v_min
      new_velocity_arr.append(new_velocity)
      j = j + 1

    self.velocity.append(new_velocity_arr)

  # Update the particle's position based on its previous velocity and position  
  def UpdatePosition(self):
    global p_max, p_min, dim
    t1 = len(self.velocity)
    t2 = len(self.pos)
        
    new_position_arr = []

    j = 0
    while j < dim:
      new_position = self.pos[t2-1][j] + self.velocity[t1-1][j]
      # If the position is smaller or larger than the bounds, change them
      if new_position > p_max:
        new_position = p_max
      elif new_position < p_min:
        new_position = p_min
      new_position_arr.append(new_position)
      j = j + 1
    self.pos.append(new_position_arr)

main()