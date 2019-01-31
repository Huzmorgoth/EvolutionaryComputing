# Created by Huzefa Shaikh

import math
import random
import numpy as np
#math functions & constants
sin=math.sin
cos=math.cos
sqrt=math.sqrt
pi=math.pi
fabs=math.fabs

#FIX (no globals)
dim=2
Xu=[]
Xl=[]
pop=[]
fvals=[]
num_fe=0 #Function-evaluation-count-total-number
max_gen=0 #number of generations
NP=15 # number of iterations (population as well)
cr=0.90 #crossover-probability
F=0.90 #Scaling-factor
U=[] #trial-vector

f_best=-1
f_worst=1
#util function- return a random real in (0.0,1.0)
def rand_n():
    
    return random.random()

#function objective 
def func(X):
    global num_fe
    sum=0

    for i in range(0,dim):
         sum = sum + X[i]*X[i];

    num_fe=num_fe+1

    return sum

# Control parameters
def setup():

    global max_gen,dim,Xu,Xl,NP,f_best,f_worst

    max_gen = input("Enter the number of runs:: ")
    dim=input("Enter the dimension of the problem:: ")

#     for i in xrange(0,dim):
#         print "Enter the lower and upper bound of %d th variable" %i
#         Xl.insert(i,input())
#         Xu.insert(i,input())

    print ("Enter the lower and upper bound of variables: ")
    l = input()
    u = input()
    for i in range(0,dim):
        Xl.insert(i,l)
        Xu.insert(i,u)

    #NP=20*dim #population size

    # Open the file to store the best individual of every generation
    f_best=open("best-population.out","w")
    #f_worst=open("worst-population.out","w")

#Initialize-population
def initpop():

    global pop,fvals,num_fe

    pop=[]
    fvals=[]

    for i in range(0,NP):
        X=[]
        for j in range(0,dim):
            #fill-up-X-add-population
            X.insert(j,(Xl[j] + (Xu[j]-Xl[j])*rand_n()))


        #bounds-check
        for j in range(0,dim):
            while X[j] < Xl[j] or X[j] > Xu[j]:
                if X[j]<Xl[j]:
                    X[j]=2*Xl[j]-X[j]
                if X[j]>Xu[j]:
                    X[j]=2*Xu[j]-X[j]


        pop.insert(i,X)
        fvals.insert(i,func(X)) #function-evaluation


#DE/rand/1
def evolve_de_rand_1():

    global pop,fvals

    for i  in range(0,max_gen):
        
        #Write the best individual of this generation into a file
        
        #best_pop.out
        write_best()
        for j in range(0,NP):


            #MUTATION
            
            while 1:
                r1=random.randint(0,NP-1)
                if r1!=j:
                    break
            
            while 1:
                r2=random.randint(0,NP-1)
                if r2!=r1 and r2!=j:
                    break

            while 1:
                r3=random.randint(0,NP-1)
                if r3!=r2 and r3!=r1 and r3!=j:
                    break

            U=[]
            for k in range(0,dim):
                #if rand_n() <= cr and k == dim_rand:
                U.insert(k,(pop[r3])[k] + F*((pop[r1])[k]-(pop[r2])[k]))
                
            #CROSSOVER
            n = int(rand_n()*dim)
            L=0
            while 1:
                L=L+1
                if rand_n() > cr or L>dim:
                    break
            
            for k in range(0,dim):
                for kk in (n,n+L):
                    if k != (kk % dim):
                        U.insert(k,(pop[j])[k])
        
            
            #BOUNDS-CHECK
            for k in range(0,dim):
                while U[k] < Xl[k] or U[k] > Xu[k]:
                    if U[k]<Xl[k]:
                        U[k]=2*Xl[k]-U[k]
                    if U[k]>Xu[k]:
                        U[k]=2*Xu[k]-U[k]
                        

            U.insert(dim,func(U)) #the function value (the-last-value)
            
            #SELECTION
            #Comparing the trial vector and past individual
            if U[dim] <= fvals[j]:
                for k in range(0,dim):
                  (pop[j])[k]=U[k]
                fvals.insert(j,func(pop[j]))


#Find the best objective func. value and write it to the file

#accessed all generation
def write_best():
    best_val=fvals[0]
    worst_val=fvals[0]
    best_index=0
    for i in range(0,NP):
        if fvals[i] < best_val:
            best_index=i
            best_val=fvals[i]
        else:
            best_index=i
            worst_val=fvals[i]

    f_best.write(str(best_val))
    f_best.write('\n')
    #f_worst.write(str(worst_val))
    #f_worst.write('\n')        
#Report the best pop and save the population 
#STATs
def report():    

    #Save the final population to the file
    f=open("final_population.out","w")
    f.write("Final Population Data: Variable Values -- Objective Function Values\n")
    for i in range(0,NP):
        for j in range(0,dim):
            f.write(str((pop[i])[j]) + '\t')
        f.write('\t\t|| ')
        f.write(str(fvals[i]))
        f.write('\n')
    f.close()
    
    #Find the best individual and report
    best_val=fvals[0]
    best_index=0
    worst_index=0
    results = []
    popss = []
    for i in range(0,NP):
        popss.append(pop[i])
        results.append(fvals[i])
        if fvals[i] < best_val:
            best_index=i
            best_val=fvals[i]
    
    for wi in range(0,NP):
        if fvals[wi] > best_val:
            worst_index=wi
            best_val=fvals[wi]
    
    nres = np.array(results)        
    

    print results,',',popss
    print '\nBest : ',fvals[best_index],'--:--',pop[best_index]
    print '\nWorst : ',fvals[worst_index],'--:--',pop[worst_index]
    print '\naverage : ',np.mean(nres)

    print 'function-evaluations-total-number : ', num_fe


if __name__ =='__main__':

    print("Differential-Evolution->>>")
    print("-----------------------------------------")
    setup()
    initpop()
    print("Evolution-process-running..")
    evolve_de_rand_1()
    print("\nSUMMARY")
    print("-----------------------\n")
    report()