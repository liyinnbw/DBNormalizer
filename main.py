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
R = ['program_id','project_id', 'project_application_id','talent_id','experience_id','hearabout_id', 'program_application_status','project_application_status']
FD = [
    [['talent_id'],['program_id', 'program_application_status']],
    [['experience_id'],['talent_id','project_id']],
    [['project_application_id'],['talent_id', 'program_id', 'project_id', 'project_application_status']],
    [['hearabout_id'],['program_id','talent_id']],
    [['project_id'],['program_id']],
]
normalform = normalforms.threenf
# Do not modify anything from this line onwards

###########################################
# find all candidate keys
###########################################
print('all candiate keys:')
print (api.candidate_keys(R, FD))

###########################################
# find a minimal cover
###########################################
print('')
print('')
print('a minimal cover:')
minCover = api.min_cover(R,FD)
for F in minCover:
    print(F)

###########################################
# check all F in FD for violation of given normal form
###########################################
print('')
print('')  
print('check normal form:',normalform.__name__)
FDsimplified = api.min_cover_step1(R,FD)
for F in FDsimplified:
    print(F,normalform(R,FDsimplified,F))


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
# synthesize to given normal form
# also check wether synthesize is dependency-preserving
# if not show which dependency is lost
# also verify result against given normal form
###########################################
printStep = False # if true will print steps invovled in deriving the answer
print('')
print('')
print('synthesis:', normalform.__name__, 'showStep' if printStep else '')
fragments = decomposition.simple_synthesis(R,FD,printStep)
decomposition.print_fragments(fragments,normalform)


