import api
import normalforms
import decomposition

########################################### 
# R is a list of unique variables (R =['A','B','C'])

# F is a list of functional dependencies. 
# Each dependency in F consists of two lists, where the former implies the latter
# For example: A->BC is [['A'],['B','C']]

# normalform defines which normal form you want to achieve
# it can be any of the following:
# (2NF) normalforms.twonf
# (3NF) normalforms.threenf
# (BCNF) normalforms.bcnf
###########################################

# Modify from this line onwards to suit your needs
R = ['A', 'B', 'C']
FD = [[['A', 'B'], ['C']], [['A'], ['B']], [['B'], ['A']]]
normalform = normalforms.threenf
# Do not modify anything from this line onwards

###########################################
# find all candidate keys
###########################################
print('all candiate keys:')
print(api.candidate_keys(R, FD))

###########################################
# find a minimal cover
###########################################
print('')
print('')
print('a minimal cover:')
minCover = api.min_cover(R,FD)
for F in minCover:
    print(F[0],'->',F[1])

###########################################
# check all F in FD for violation of given normal form
###########################################
print('')
print('')  
print('check normal form:',normalform.__name__)
FDsimplified = api.min_cover_step1(R,FD)
for F in FDsimplified:
    print(F[0],'->',F[1],normalform(R,FDsimplified,F))


###########################################
# decomposition to given normal form
# also check wether decomposition is dependency-preserving
# if not show which dependency is lost
# also verify result against given normal form
###########################################
useSigmaPlus = True
printStep = False # if true will print steps invovled in deriving the answer
print('')
print('')
print('decomposition:',normalform.__name__, 'showStep' if printStep else '')
fragments = decomposition.decompose(R,FD,normalform,useSigmaPlus,printStep)
decomposition.print_fragments(fragments,normalform)

###########################################
# synthesize to 3NF (not any form)
# also check wether synthesize is dependency-preserving
# if not show which dependency is lost
# also verify result against 3NF
###########################################
printStep = False # if true will print steps invovled in deriving the answer
print('')
print('')
print('synthesis: threenf', 'showStep' if printStep else '')
fragments = decomposition.simple_synthesis(R,FD,printStep)
decomposition.print_fragments(fragments,normalform)


