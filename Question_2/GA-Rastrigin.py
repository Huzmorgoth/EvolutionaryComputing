# Created by Huzefa Shaikh

from pyevolve import Mutators, Initializators
from pyevolve import Selectors
import math
from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Consts
import numpy as np
#Rastrigin function intitiation
def rast(gen):
   total_ret = 0
   len_genome = len(gen)
   for i in range(len_genome):
      total_ret += gen[i]**2 - 10*math.cos(2*math.pi*gen[i])
   return (10*len_genome) + total_ret

def algorith_run():

  lr = 0.06
  results = []
  for x in range(15):

   #Genome structure
   gen = G1DList.G1DList(2)
   gen.setParams(rangemin=-5.2, rangemax=5.30, bestrawscore=0.00, rounddecimal=2)
   gen.initializator.set(Initializators.G1DListInitializatorReal)
   gen.mutator.set(Mutators.G1DListMutatorRealGaussian)

   gen.evaluator.set(rast)

   #Genetic Algorithm
   gen_Algo = GSimpleGA.GSimpleGA(gen)
   gen_Algo.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
   gen_Algo.setMinimax(Consts.minimaxType["minimize"])
   gen_Algo.setGenerations(300)
   gen_Algo.setCrossoverRate(0.8)
   gen_Algo.setPopulationSize(50)
   gen_Algo.setMutationRate(lr)
   lr += 0.01
   gen_Algo.evolve(freq_stats=40)

   #print 'Run: ',x,'\n'
   exec_best = gen_Algo.bestIndividual()
   print exec_best
   results.append(exec_best)
   print '\n'

  minn = min(results)
  maxx = max(results)
  nresult = np.array(results)
  meann = np.mean(nresult)

  print 'Best Performacne: ', minn
  print 'Worst Performacne: ', maxx
  print 'Average of all the performance', meann
  
  return 

if __name__ == "__main__":
   algorith_run()