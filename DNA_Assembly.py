# Author:PAUL COZMUTA

import random

#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 1: RANDOM SHUFFLING OF LIST ELEMENTS
#----------------------------------------------------------------------------------------------------------------------------------------
"""
-What the function does: randomly shuffles the positions of the list
-Inputs: the list to shuffle
-Outputs: the shuffled list
"""


def unsort(l):
    return random.sample(l, len(l))


#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 2: FILE READING
#----------------------------------------------------------------------------------------------------------------------------------------
"""
-What the function does: reads the file of interest and creates a list with its elements
-Inputs: the file name as a string
-Outputs: a list with the file's elements
"""

def lee(fichero):
    S=[]
    with open(fichero, "r") as tf:
        lines = tf.read().split('\n')
    lines=list(lines)
    for i in lines:
        if len(i) != 0:
            S.append(str(i))
    return S


#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 3: RANDOM CREATION OF THE POPULATION OR ITS REPOPULATION
#----------------------------------------------------------------------------------------------------------------------------------------   
"""
-What the function does: creates a population of random possible Hamiltonian paths. It also fills a population until it consists of 30
individuals.
-Inputs: the list of elements and the list containing the current population of possible paths
-Outputs: a new population of 30 individuals
"""

def crea_renueva_poblacion(S,pob_actual,numero):

    orden=[]
    for i in range(0,len(S)):
        orden.append(i)
    while len(pob_actual)<numero:
        b=unsort(orden)
        pob_actual.append(b)
    return pob_actual


#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 4: CONVERTING HAMILTONIAN PATHS TO STRINGS
#----------------------------------------------------------------------------------------------------------------------------------------
"""
-What the function does: joins the elements of a list in order, maximizing the overlap.
-Inputs: the list to join.
-Outputs: a string that is a superstring.
"""

def string(lista):

    contador=0
    L=len(lista[0])
    if contador < L:
        for i in range(0,L):
            contador=contador+1
            if len(lista[0][i:]) <= len(lista[1]):
                if lista[0][i:] == lista[1][0:len(lista[0][i:])]:
                    nueva= lista[0][0:i]+lista[1]
                    lista.remove(lista[1])
                    lista[0]=nueva
                    if len(lista)>1:
                        supercadena=string(lista)
                    supercadena="".join(lista)
                    return supercadena
    if contador == L:
        nueva= lista[0]+lista[1]
        lista.remove(lista[1])
        lista[0]=nueva
        if len(lista)>1:
            supercadena=string(lista)
        supercadena="".join(lista)
        return supercadena


#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 5: ASSIGNING FITNESS VALUE TO EACH HAMILTONIAN PATH IN THE POPULATION
#----------------------------------------------------------------------------------------------------------------------------------------
"""
-What the function does: assigns a fitness value to each individual and returns a list with all of them
-Inputs: the population of paths contained in a list and the list containing the S fragments.
-Outputs: a list with the fitness values for each individual in the population.
"""

def fitness(S,poblacion):
    fi_total=0
    lista=[]
    long=[]
    for j in poblacion:
        lista2=[]
        for pos in j:
            lista2.append(S[pos])    
        fi_total=fi_total+len(string(lista2))  
    for e in poblacion:
        liston=[]
        for a in e:
            liston.append(S[a])
        lista.append(string(liston))
    for w in lista:
        long.append(len(w)/fi_total)
    return long


#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 6: SWAPPING POSITIONS OF ELEMENTS IN A LIST
#----------------------------------------------------------------------------------------------------------------------------------------
"""
-What the function does: swaps the positions of elements in a list
-Inputs: the two positions we want to swap
-Outputs: a list with the elements swapped
"""

def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
        

#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 7: MUTATIONS IN THE ORDER OF HAMILTONIAN PATHS
#----------------------------------------------------------------------------------------------------------------------------------------
"""
-What the function does: introduces mutations with a certain probability and if favorable in the Hamiltonian paths of the current population
-Inputs: the population of possible Hamiltonian paths
-Outputs: a list containing the entire population with or without mutations.
"""


def mutaciones(S,poblacion):
    
    for a in range(0,len(poblacion)):
        i=poblacion[a]

        """Random mutations"""
        probabilidad2=0.3
        nro=random.random()
        n1=random.randint(0, len(S)-1)
        n2=random.randint(0,len(S)-1)
        if nro <= probabilidad2:
            poblacion[a]=swapPositions(i,n1,n2)
        
        """Mutaciones invirtiendo el individuo"""
        probabilidad3=0.15
        nro2=random.random()
        if nro2 <= probabilidad3:
            poblacion[a]=list(reversed(poblacion[a]))
    return poblacion


#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 8: INTRODUCING DELETIONS IN THE POPULATION
#----------------------------------------------------------------------------------------------------------------------------------------        
"""
-What the function does: introduces deletions among the different individuals in the population. In this case, the algorithm does not 
consider favorable deletions; they are performed randomly.
-Inputs: the list of the population of Hamiltonian paths to which the deletions are applied
-Outputs: a list with the population after the deletions have been carried out.
"""

def recombinaciones(poblacion):
    for a in range(0,len(poblacion)):
        probabilidad=0.8
        numero_asignado=random.random()
        if numero_asignado <= probabilidad:
            elemento=random.randint(0, len(poblacion)-1)
            posicion_elemento=random.randint(0, len(poblacion[elemento])-1)
            posicion_a=random.randint(0,len(poblacion[a])-1)
            if posicion_elemento == posicion_a:
                trozo_elemento_2=poblacion[elemento][posicion_elemento:]
                trozo_a_2=poblacion[a][posicion_a:]
                trozo_elemento_1=poblacion[elemento][0:posicion_elemento]
                trozo_a_1=poblacion[a][0:posicion_a]
                cont=0
                for i in trozo_elemento_2:
                    if i in trozo_a_2:
                        cont=cont+1
                if cont == len(trozo_elemento_2):
                    poblacion[a]=trozo_a_1 + trozo_elemento_2
                    poblacion[elemento]= trozo_elemento_1 + trozo_a_2
    return poblacion
                

#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 9: SELECTION OF INDIVIDUALS WITH THE BEST FITNESS
#----------------------------------------------------------------------------------------------------------------------------------------        
"""
-What the function does: selects a subset of paths from the population with the best fitness
-Inputs: the population to select from, provided as a list
-Outputs: a list of individuals or an individual with the best fitness
"""

def selecciona(S,poblacion,cantidad):
    orden_fitness=[]
    f=fitness(S,poblacion)
    while len(orden_fitness)<len(f):
        valor=0
        pos=0
        for i in range(0,len(f)):
            if f[i] != 0:
                if f[i] >= valor:
                    pos=i
                    valor=f[i]
        orden_fitness.append(poblacion[pos])
        f[pos]=0

    cont=0
    elegidos=[]
    for i in range(len(orden_fitness)-1,-1,-1):
        if orden_fitness[i] in elegidos:
            continue
        else:
            cont=cont+1
            elegidos.append(orden_fitness[i])
        if cont == cantidad:
            return elegidos
            
        
        
#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTION 10: USING ALL PREVIOUS FUNCTIONS TO ACHIEVE THE FINAL FUNCTION
#----------------------------------------------------------------------------------------------------------------------------------------        
"""
-What the function does: uses all the previous functions to generate the final algorithm.
-Inputs: the file to read
-Outputs: a more optimal superstring and its length.
"""

def SSP_genetic_algorithm(fichero,fichero2):
    
    S=lee(fichero)
    poblacion_actual=[]
    for i in range(20,0,-1):
        poblacion_actual=crea_renueva_poblacion(S,poblacion_actual,30)
        poblacion_actual=mutaciones(S,poblacion_actual)
        poblacion_actual=recombinaciones(poblacion_actual)
        poblacion_actual=selecciona(S,poblacion_actual,i)
    
    palabraa=[]
    for j in poblacion_actual[0]:
        palabraa.append(S[j])
    
    supercadena=string(palabraa) 

    with open(fichero2, 'w') as file:
        file.write(supercadena)
    print(f"File {fichero2} created successfully!")


#----------------------------------------------------------------------------------------------------------------------------------------
#MAIN
#----------------------------------------------------------------------------------------------------------------------------------------        
def main():
    
  fichero=str(input('Please introduce the reads file name:'))
  fichero2=str(input('Please introduce the output DNA sequence file name:'))
  SSP_genetic_algorithm(fichero,fichero2)
  
if __name__ == "__main__":
    main()




                
                    
                    
                    
                    
                    
                
                
        
        
    
 
            
            
    