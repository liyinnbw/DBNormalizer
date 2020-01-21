import itertools
from itertools import combinations
from itertools import permutations

# Determine the closure of set of attribute S given the schema R and functional dependency F
def closure(R, F, S):
    unused = [True for f in F]
    closureSet = set(S)  # copy
    fIdx = 0
    while fIdx < len(F):
        if unused[fIdx] and set(F[fIdx][0]) <= closureSet:
            for a in F[fIdx][1]:
                closureSet.add(a)
            unused[fIdx] = False
            fIdx = 0
        else:
            fIdx += 1
    result = list(closureSet)
    return result

# Determine the all the attribute closure excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F):
    allClosures = []
    # sort R so that subsets will be sorted
    R.sort()
    # If the input iterable is sorted, the combination tuples will be produced in sorted order.
    allSubSets = [list(x) for x in sum(
        map(lambda r: list(combinations(R, r)), range(1, len(R)+1)), [])]
    candidateKeys = []
    for S in allSubSets:
        Sset = set(S)
        Splus = closure(R, F, S)
        Splus.sort()
        if len(Splus) == len(R):
            isSuperKey = False
            for candidate in candidateKeys:
                if candidate < Sset:
                    isSuperKey = True
                    break
            if not isSuperKey:
                candidateKeys.append(Sset)
                allClosures.append([S, Splus])
        else:
            allClosures.append([S, Splus])
    return allClosures

# Return the candidate keys of a given schema R and functional dependencies F.
# return sets of candidate keys
def candidate_keys(R, F):
    # sort R so that subsets will be sorted
    Rsort = sorted(R)
    # If the input iterable is sorted, the combination tuples will be produced in sorted order.
    allSubSets = [list(x) for x in sum(
        map(lambda r: list(combinations(Rsort, r)), range(1, len(Rsort)+1)), [])]
    candidateKeys = []
    for S in allSubSets:
        Sset = set(S)
        Splus = closure(Rsort, F, S)
        if len(Splus) == len(Rsort):
            isSuperKey = False
            for candidate in candidateKeys:
                if candidate < Sset:
                    isSuperKey = True
                    break
            if not isSuperKey:
                candidateKeys.append(Sset)
    return candidateKeys #[list(s) for s in candidateKeys] 

###########################################
# helper functions for min_cover


# step 1: reduce RHS to singleton
def min_cover_step1(R, FD):
    newFD = []
    for F in FD:
        if len(F[1]) > 0:
            for a in F[1]:
                newFD.append([F[0], [a]])
        else:
            newFD.append(F)
    return newFD

# Given R, FD and one functional depency X->Y in FD where Y contains only single attribute
# simplify X by testing attributes in X from left to right in order.
# Return the simplified functional depenency in the format [[X],[Y]]


def simplifyX(R, FD, X, Y):
    shouldKeep = [True for a in X]
    for idx in range(len(X)):
        if not shouldKeep[idx]:
            continue
        otherAttribsLeft = [X[i]
                            for i in range(len(X)) if (i != idx and shouldKeep[i])]
        otherAttribsClosure = closure(R, FD, otherAttribsLeft)
        if (Y[0] in otherAttribsClosure) or (X[idx] in otherAttribsClosure):
            # attrib is redundant
            shouldKeep[idx] = False
    simplifiedX = [X[idx] for idx in range(len(X)) if shouldKeep[idx]]
    return [simplifiedX, Y]

# step 2: simplify LHS
# prerequisite: RHS of any F in FD only contains single attribute


def min_cover_step2(R, FD):
    newFD = []
    for F in FD:
        newFD.append(simplifyX(R, FD, F[0], F[1]))
    return newFD

# step 3: remove redundancy
# elimination follows the ordering of F in FD


def min_cover_step3(R, FD):
    shouldKeep = [True for F in FD]
    for idx, F in enumerate(FD):
        # temporarily remove F
        shouldKeep[idx] = False
        otherFs = [FD[x] for x in range(len(FD)) if shouldKeep[x]]
        if F[1][0] not in closure(R, otherFs, F[0]):
            shouldKeep[idx] = True
    newFD = [FD[x] for x in range(len(FD)) if shouldKeep[x]]
    # for unique representation
    for F in newFD:
        F[0].sort()
    newFD.sort()
    return newFD

###########################################

# Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD):
    return min_cover_step3(R, min_cover_step2(R, min_cover_step1(R, FD)))

# Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
def min_covers(R, FD):
    # step1: simplify RHS
    FD1 = min_cover_step1(R, FD)
    # step2: simplify LHS
    possibleFD2s = []
    for F in FD1:
        # there are multiple ways of simplifying the LHS of an F
        # instead of trying just one permutation, we try them all
        # and keep all possible outcomes in possibleSimplifiedFs
        LHSpermutes = [list(x) for x in permutations(F[0])]
        possibleSimplifiedFs = []
        for X in LHSpermutes:
            simplifiedF = simplifyX(R, FD, X, F[1])
            if len(simplifiedF[0]) == len(F[0]):
                # skip trivial
                if F[1][0] not in simplifiedF[0]:
                    simplifiedF[0].sort()  # ensure unique representation
                    if simplifiedF not in possibleSimplifiedFs:
                        possibleSimplifiedFs.append(simplifiedF)
                # LHS can't be simplified, no need to consider other permutations
                break
            else:
                # skip trivial
                if F[1][0] not in simplifiedF[0]:
                    simplifiedF[0].sort()  # ensure unique representation
                    if simplifiedF not in possibleSimplifiedFs:
                        possibleSimplifiedFs.append(simplifiedF)
        if len(possibleSimplifiedFs) > 0:
            # possibleFD2s contains a list of list of simplified Fs
            possibleFD2s.append(possibleSimplifiedFs)

    # transform possibleFD2s into list of possible FD2s
    FD2s = list(itertools.product(*possibleFD2s))
    FD2uniques = []
    for FD2 in FD2s:
        FD2unique = []
        for F in FD2:
            if F not in FD2unique:
                FD2unique.append(F)
        if FD2unique not in FD2uniques:
            FD2uniques.append(FD2unique)

    # step3: remove redundancy
    result = []
    for FD2 in FD2uniques:
        FD3s = [list(x) for x in permutations(FD2)]
        # print (len(FD2),'! =', len(FD3s))
        for fd in FD3s:
            # method 1: most direct and simple way
            mincover = min_cover_step3(R, fd)
            mincover.sort()
            if mincover not in result:
                result.append(mincover)
    result.sort()

    # # alternative step 2 onwards
    # FD2 = []
    # for F in FD1:
    #     # there are multiple ways of simplifying the LHS of an F
    #     # instead of trying just one permutation, we try them all
    #     # and keep all possible outcomes in FD2
    #     LHSpermutes = [list(x) for x in permutations(F[0])]
    #     for X in LHSpermutes:
    #         simplifiedF = simplifyX(R,FD,X,F[1])
    #         if len(simplifiedF[0]) == len(F[0]):
    #             # skip trivial
    #             if F[1][0] not in simplifiedF[0]:
    #                 simplifiedF[0].sort() # ensure unique representation
    #                 if simplifiedF not in FD2:
    #                     FD2.append(simplifiedF)
    #             # LHS can't be simplified, no need to consider other permutations
    #             break
    #         else:
    #             # skip trivial
    #             if F[1][0] not in simplifiedF[0]:
    #                 simplifiedF[0].sort() # ensure unique representation
    #                 if simplifiedF not in FD2:
    #                     FD2.append(simplifiedF)

    # # find all permutations of FD2
    # FD3s = [list(x) for x in permutations(FD2)]
    # # print (len(FD2),'! =', len(FD3s))
    # result = []
    # for fd in FD3s:
    #     mincover = min_cover_step3(R, fd)
    #     mincover.sort()
    #     if mincover not in result:
    #         result.append(mincover)
    # result.sort()
    return result

# Return all minimal covers of a given schema R and functional dependencies F.
def all_min_covers(R, FD):
    # all_closures() produce result in increasing LHS size and sorted LHS
    # which is necessary for the following algo to work
    allClosures = all_closures(R, FD)
    # create a dictionary for O(1) attribute closure access, using LHS as key
    closureDic = {}
    for C in allClosures:
        closureDic[tuple(C[0])] = C[1]

    minimalFs = []
    for C in allClosures:
        # construct FD by keeping RHS single attribute
        for A in C[1]:
            # skip if RHS contained in LHS
            # this means the F will be trivial if included
            if A in C[0]:
                continue
            # skip if RHS contained in closure of proper subsets of LHS
            # this means the F is already covered by previous F
            # we just need to consider minus-1 subsets
            shouldKeep = True
            for i in range(len(C[0])):
                otherAttribs = C[0][:i] + C[0][i+1:]
                otherAttribsClosure = closureDic.get(tuple(otherAttribs))
                if otherAttribsClosure != None and A in otherAttribsClosure:
                    shouldKeep = False
                    break
            if shouldKeep:
                minimalFs.append([C[0], [A]])

    # find all permutations of minimalFs
    possibleFDs = [list(x) for x in permutations(minimalFs)]
    # print (len(minimalFs),'! =', len(possibleFDs))
    result = []
    for fd in possibleFDs:
        mincover = min_cover_step3(R, fd)
        mincover.sort()
        if mincover not in result:
            result.append(mincover)
    result.sort()
    return result

def equivalent(R, FD1, FD2):
    closures1 = all_closures(R,FD1)
    closures2 = all_closures(R,FD2)
    closures1.sort()
    closures2.sort()
    return closures1 == closures2

def get_lost_dependencies(R, FD1, FD2):
    lostDependencies = []
    for F in FD1:
        C = closure(R,FD2,F[0])
        if not set(F[1])<=set(C):
            lostDependencies.append(F)
    return lostDependencies
    

# # Test case from the project
# R = ['A', 'B', 'C', 'D']
# FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

# print (closure(R, FD, ['A']))
# print (closure(R, FD, ['A', 'B']))
# print (all_closures(R, FD))
# print (candidate_keys(R, FD))

# R = ['A', 'B', 'C', 'D', 'E', 'F']
# FD = [[['A'], ['B', 'C']], [['B'], ['C', 'D']],
#       [['D'], ['B']], [['A', 'B', 'E'], ['F']]]
# print (min_cover(R, FD))

# R = ['A', 'B', 'C']
# FD = [[['A', 'B'], ['C']], [['A'], ['B']], [['B'], ['A']]]
# print (min_covers(R, FD))
# print (all_min_covers(R, FD))

# # Tutorial questions
# R = ['A', 'B', 'C', 'D', 'E']
# FD = [[['A', 'B'], ['C']], [['D'], ['D', 'B']], [['B'], ['E']],
#       [['E'], ['D']], [['A', 'B', 'D'], ['A', 'B', 'C', 'D']]]

# print (candidate_keys(R, FD))
# print (min_cover(R, FD))
# print (min_covers(R, FD))
# print (all_min_covers(R, FD))
