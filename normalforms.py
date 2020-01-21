import api

def bcnf(R, FD, F, candidateKeySets = None):
    if len(F) == 0:
        return True
    if len(F[1])>1:
        print('RHS must be of length 1')
        return False

    if candidateKeySets is None:
        candidateKeySets = api.candidate_keys(R, FD)
    X = set(F[0])
    A = F[1][0]
    
    # X->A is trival ie A is subset of X
    if A in X:
        return True
    # X is a superkey
    for ck in candidateKeySets:
        if X>=ck:
            return True
    return False

def threenf(R, FD, F, candidateKeySets = None):
    if len(F) == 0:
        return True
    if len(F[1])!=1:
        print('RHS must be of length 1')
        return False

    if candidateKeySets is None:
        candidateKeySets = api.candidate_keys(R, FD)
    X = set(F[0])
    A = F[1][0]

    # X->A is trival ie A is subset of X
    if A in X:
        return True
    # X is superkey
    for ck in candidateKeySets:
        if X>=ck:
            return True
    # A is prime attribute
    for ck in candidateKeySets:
        if A in ck:
            return True 
    return False

def twonf(R, FD, F, candidateKeySets = None):
    if len(F) == 0:
        return True
    if len(F[1])!=1:
        print('RHS must be of length 1')
        return False

    if candidateKeySets is None:
        candidateKeySets = api.candidate_keys(R, FD)
    X = set(F[0])
    A = F[1][0]

    # X->A is trival ie A is subset of X
    if A in X:
        return True
    # X is NOT a proper subset of a ck
    for ck in candidateKeySets:
        if not X<ck:
            return True
    # A is prime attribute
    for ck in candidateKeySets:
        if A in ck:
            return True 
    return False

def check(R, FD, normalform):
    print('check',normalform.__name__)
    candidateKeySets = api.candidate_keys(R, FD)
    for F in FD:
        print(F, normalform(R, FD, F, candidateKeySets))


# S1 = set(['A','B'])
# S2 = set(['A','C'])
# S3 = set(['D'])
# S4 = set(['A','B'])
# S5 = set(['A','B','C'])

# print (S2<S1, S2>=S1)
# print (S3<S1, S3>=S1)
# print (S4<S1, S4>=S1)
# print (S5<S1, S5>=S1)