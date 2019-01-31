# created by Huzefa Shaikh

from pyevolve import G1DList
from pyevolve import Mutators, Initializators
from pyevolve import GSimpleGA, Consts
import numpy as np

# Sphere-Function
def sphere(xlist):
   total = 0
   for i in xlist:
      total += i**2
   return total

def run_main():

  lr = 0.01
  results = []
  for x in range(15):

    genome = G1DList.G1DList(2)
    genome.setParams(rangemin=-5.12, rangemax=5.13)
    genome.initializator.set(Initializators.G1DListInitializatorReal)
    genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
    genome.evaluator.set(sphere) # Call sphere function
    
    # Configure Genetic Algorith
    ga = GSimpleGA.GSimpleGA(genome, seed=666)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(300)
    ga.setMutationRate(lr)
    lr += 0.01
    ga.evolve(freq_stats=100)
    
    #print best individual
    #print 'Run: ',x,'\n'
    best = ga.bestIndividual()
    print best
    results.append(best)
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

    run_main()
    