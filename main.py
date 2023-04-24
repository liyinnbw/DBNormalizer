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
# R = ['A', 'B', 'C', 'D']
# FD = [[['B', 'C'], ['D']], [['A'], ['B']]]
# normalform = normalforms.bcnf
R = input("Enter the list of unique variables of R separated by commas (e.g. a,b,c,d): ").split(",")
FD = []
while True:
    dep = input("Enter a functional dependency (e.g. a,b->c) or enter nothing to stop: ")
    if not dep:
        break
    try:
        lhs, rhs = dep.split("->")
        FD.append([lhs.split(","), rhs.split(",")])
    except ValueError:
        print("Invalid functional dependency! Reenter the functional dependency.")
while True:
    normalform_name = input("Enter the normal form you want to achieve (2nf, 3nf, or bcnf): ")
    if normalform_name == "2nf":
        normalform = normalforms.twonf
        break
    elif normalform_name == "3nf":
        normalform = normalforms.threenf
        break
    elif normalform_name == "bcnf":
        normalform = normalforms.bcnf
        break
    else:
        print("Invalid normal form! Reenter the normal form.")

# Do not modify anything from this line onwards

###########################################
# find all candidate keys
###########################################
print('all candidate keys:')
print(api.candidate_keys(R, FD))

###########################################
# find a minimal cover
###########################################
print('')
print('')
print('a minimal cover:')
minCover = api.min_cover(R, FD)
for F in minCover:
    print(F[0], '->', F[1])

###########################################
# check all F in FD for violation of given normal form
###########################################
print('')
print('')
print('check normal form:', normalform.__name__)
FDsimplified = api.min_cover_step1(R, FD)
for F in FDsimplified:
    print(F[0], '->', F[1], normalform(R, FDsimplified, F))

###########################################
# decomposition to given normal form
# also check whether decomposition is dependency-preserving
# if not show which dependency is lost
# also verify result against given normal form
###########################################
useSigmaPlus = True
printStep = False  # if true will print steps involved in deriving the answer
print('')
print('')
print('decomposition:', normalform.__name__, 'showStep' if printStep else '')
fragments = decomposition.decompose(R, FD, normalform, useSigmaPlus, printStep)
decomposition.print_fragments(fragments, normalform)

###########################################
# synthesize to 3NF (not any form)
# also check whether synthesize is dependency-preserving
# if not show which dependency is lost
# also verify result against 3NF
###########################################
printStep = False  # if true will print steps involved in deriving the answer
print('')
print('')
print('synthesis: threenf', 'showStep' if printStep else '')
fragments = decomposition.simple_synthesis(R, FD, printStep)
decomposition.print_fragments(fragments, normalform)
