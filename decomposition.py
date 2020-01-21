import api
import normalforms


def projtect_dependency(FD, R):
    projectedF=[]
    for F in FD:
        shouldKeep = True
        for a in F[0]:
            if a not in R:
                shouldKeep = False
                break
        if shouldKeep:
            for a in F[1]:
                if a not in R:
                    shouldKeep = False
                    break
        if shouldKeep:
            projectedF.append(F)
    return projectedF


def decompose_into_fragments(R, FD, F):
    R1 = api.closure(R,FD, F[0])
    R2 = [x for x in R if x not in R1]
    R2.extend(F[0])
    R1.sort()
    R2.sort()
    FD1 = projtect_dependency(FD, R1)
    FD2 = projtect_dependency(FD, R2)
    return R1, R2, FD1, FD2


def should_add(fragments, newfrag):
    newR = set(newfrag[0])
    for frag in fragments:
        R = set(frag[0])
        if newR<=R:
            # already has a super set
            return False
    return True
        


def decompose(R, FD, normalform, useSigmaPlus = False, printStep = False):
    sigma =[]
    if useSigmaPlus:
        # find sigma plus
        closures = api.all_closures(R, FD)
        for C in closures:
            for A in C[1]:
                if A in C[0]:
                    continue
                F = [C[0],[A]]
                if F not in sigma:
                    sigma.append(F)
    else:
        # simplify RHS if not done so
        for Fo in FD:
            LHS = sorted(Fo[0])
            for A in Fo[1]:
                if A in LHS:
                    continue
                F = [LHS,[A]]
                if F not in sigma:
                    sigma.append(F)


    notDone =[[R,sigma]]
    done =[]


    while len(notDone)>0:
        fragment = notDone[0]
        isGood = True
        for F in fragment[1]:
            if not normalform(fragment[0], fragment[1], F):
                # found violation
                isGood = False
                R1, R2, FD1, FD2 = decompose_into_fragments(fragment[0], sigma, F)
                notDone = [[R1,FD1],[R2, FD2]]+notDone[1:]
                break
        if isGood: 
            if should_add(done,fragment):
                done.append(fragment)
            notDone = notDone[1:]
        if printStep:
            print('~~DONE~~')
            print_fragments(done, normalform)
            print('~~NOT DONE~~')
            print_fragments(notDone, normalform)
            print()
    
    newFD = []
    for fragment in done:
        newFD.extend(fragment[1])
    lostDependencies = api.get_lost_dependencies(R,FD,newFD)
    if len(lostDependencies)>0:
        print('lost dependencies:')
        for F in lostDependencies:
            print(F)
    else:
         print ('dependency-preserving')

    return done

def simple_synthesis(R,FD, printStep = False):
    ckSets = api.candidate_keys(R,FD)

    # check if already in 3NF
    needToSynthesis = False
    # simplifyRHS
    simplifiedFD = api.min_cover_step1(R,FD)
    for F in simplifiedFD:
        if not normalforms.threenf(R,simplifiedFD,F,candidateKeySets=ckSets):
            needToSynthesis = True
            break
    
    if not needToSynthesis:
        print('already in 3NF')
        return [[R,simplifiedFD]]

    mincover = api.min_cover(R,FD)
    mincover.sort()
    extendedMincover = {}
    for F in mincover:
        LHStuple = tuple(F[0])
        if LHStuple not in extendedMincover:
            extendedMincover[LHStuple] = F
        else:
            extendedMincover[LHStuple][1].append(F[1][0])
    mincover = extendedMincover.values()
    if(printStep):
        print('~~EXTENDED MIN COVER~~')
        for F in mincover:
            print(F)
    
    fragments =[]
    for F in mincover:
        r =set(F[0]+F[1])
        shouldAdd = True
        for idx, frag in enumerate(fragments):
            if r<=frag[0]:
                shouldAdd = False
                # subset of existing set, only add dependency
                for A in F[1]:
                    fragments[idx][1].append([F[0],[A]])
                break
            elif r>frag[0]:
                shouldAdd = False
                # superset of existing set, replace and merge dependency
                newFD = fragments[idx][1]
                for A in F[1]:
                    newFD.append([F[0],[A]])
                fragments[idx] = [r,newFD]
                break
        if shouldAdd:
            newFD = []
            for A in F[1]:
                newFD.append([F[0],[A]])
            fragments.append([r,newFD])
        if(printStep):
            print('~~Process',F)
            print_fragments(fragments,normalforms.threenf)
            print()
    
    # if none of the cks in cksets fully captured by a fragement,
    # create a new fragment contain any 1 of the ck in cksets
    ckNotInFragment = True if len(ckSets)>0 else False
    for ck in ckSets:
        for frag in fragments:
            if ck<= set(frag[0]):
                ckNotInFragment = False
                break
        if not ckNotInFragment:
            break

    if ckNotInFragment:
        # randomly pick one ck
        fragments.append([ckSets[0],[]])
        if(printStep):
            print('~~Add',ck)
            print_fragments(fragments,normalforms.threenf)
            print()

    
    for frag in fragments:
        frag[0] = list(frag[0])
        frag[0].sort()

    newFD = []
    for fragment in fragments:
        newFD.extend(fragment[1])
    lostDependencies = api.get_lost_dependencies(R,FD,newFD)
    if len(lostDependencies)>0:
        print('lost dependencies:')
        for F in lostDependencies:
            print(F)
    else:
         print ('dependency-preserving')

    return fragments

def print_fragments(fragments, normalform):
    for fragment in fragments:
        print ('====',fragment[0])
        for F in fragment[1]:
            print (F[0],'->',F[1], normalform(fragment[0],fragment[1],F))