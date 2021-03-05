from collections import OrderedDict 

"""
 committee example from the paper """


N = 2000 # yolo? needs to be higher than all agents costs

# group blameworthiness ≈ 0.390, degree of blameworthiness is ≈ 0.073
ag1 = { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 2000 }

# same as ag1 but for additional cost of 500 would vote yes
# cost of changing vote to yes is lower
ag2 = { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 500 }

""" 
Agents 3 and 4 have same beliefs as ag1 but believe that social pressure would be less
"""
# same as ag1 but social pressure only increases chance of voting yes by 3%
# social pressure won't have as much impact
ag3 = { 'pr': 60, 'marginal_pr': 3, 'marginal_cost': 100, 'join_cost': 2000 }

# same as ag1, but believed would cost n x 150 to increase probability of voting yes
# social pressure not as effective because it will be more costly
ag4 = { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 150, 'join_cost': 2000 }

# same as ag1 but believed agents started with 40% chance of voting yes
# believed higher probability of bill failing in the first place
ag5 = { 'pr': 40, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 2000 }

# same as ag1 but she voted yes 
ag6 = { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 0 }

agents = {'ag1': {'pr': 60, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 2000},
        'ag2' : { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 500 },
        'ag3' : { 'pr': 60, 'marginal_pr': 3, 'marginal_cost': 100, 'join_cost': 2000 },
        'ag4' : { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 150, 'join_cost': 2000 },
        'ag5' : { 'pr': 40, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 2000 },
        'ag6' : { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 0 }}
# how to index in: d['agent']['key in nested dict']) 

def consrtium_cost(size, in_consortium, ag):
    size * ag.marginal_cost + (ag.join_cost if in_consortium else 0)

# pr = probability on k
# k = set of all actions agent considers possible
# def epistemic_state(pr, k):


# e1 and e2 are two epistemic states
def delta_epistemic(e1, e2, outcome):
    if e1 > e2:
        max = e1 - e2
    else:
        max = 0
    return max

# Ag = (sub)set of agents
# e = epistemic state
# def cost(ag, e)

def delta_cost(ag, e1, e2, outcome):
    c1 = cost(ag, e1)
    c2 = cost(ag, e2)
    if c2 < c1:
        max_c = 0
    else:
        max_c = c2 - c1
    return (N - max) / N

def group_blame(ag, e1, e2, outcome):
    return delta_epistemic * delta_cost

# j = number of agent (int)
# ag = subset of agents (nested dictionary)
def marginal_blame(j, ag, outcome):
    # ag_j should be a key value pair where value is a dictionary
    ag_j = 'ag' + j
    if ag_j in ag:
        # group blame - group blame without agent ag_j
        group_blame(ag, e1, outcome) - group_blame(ag.pop(ag_j), e1, outcome)
    else:
        new_ag = dict(input("Enter agent info"))
        # group blame + ag_j - group blame
        group_blame(ag.update(new_ag), e1, outcome) - group_blame(ag, e1, outcome)

# TODO
#
# - define other agents
# - define other deltas
# - define marginal/group blame as functions
#
# - verify Ag = {ag_i} "group of one" blameworthiness numbers
# - verify Ag = {ag_1, ..., ag_7} "group of all" blameworthiness numbers

# epistemic state
# pr = 60%
# k = voting yes

# n x 100