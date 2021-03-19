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

# ag7 votes yes
# ag7 = 'join_cost': 0

agents = {'ag1' : ag1,
          'ag2' : ag2,
          'ag3' : ag3,
          'ag4' : ag4,
          'ag5' : ag5,
          'ag6' : ag6}
# how to index in: d['agent']['key in nested dict']) 

def consrtium_cost(size, in_consortium, ag):
    size * ag.marginal_cost + (ag.join_cost if in_consortium else 0)

# pr = probability on k
# k = set of all actions agent considers possible
# def epistemic_state(pr, k):

# epistemic state has a few parts
#
# formally: a probability function on outcomes, indexed by a kripke structure... and a kripke structure
#   i.e., E_i = (Pr_i, K_i)
#
# how should we model this in code? well.. how is it used?
#
# delta_e1,e2,phi applies pr_i([[phi]]_k_i) (i.e., gets a probability for a given outcome) [outcome difference]
# gb^c_N(Ag',e1,e2,phi) computes c(Ag,e2) and c(Ag',e1) (and calls delta_e1,e2,phi) [relative group blame]
# gb^c_N(Ag',e1,phi) does argmax over all epistemic states with finite cost [group blame]
#
# so, three things:
#
# 1. given an outcome, produce a probabiity (delta_e1,e2,phi)
# 2. given a set of agents, compute a cost (gb^c_N(Ag',e1,e2,phi))
# 3. quantify over all possible epistemic states (w/finite cost) (gb^c_N(Ag',e1,phi))

# global variable holding all epistemic states
all_states = []

class EpistemicState(object):
    def __init__(self, ag, coalition_size, in_coalition):
        global all_states
        self.ag = ag
        self.coalition_size = coalition_size
        self.in_coalition = in_coalition
        all_states.append(self)

    def pr_yes(self):
        """probabaility of yes outcome in this epistemic state"""
        # eg. 5% increase by social pressure (n x 5%)
        coalition_boost = self.coalition_size * self.ag.marginal_pr

        # is this the right computation, or do we need to ask the probability of a final "yes" vote given the probabilities for each person?
        return self.ag.pr + coalition_boost

    def pr_no(self):
        """probabaility of no outcome in this epistemic state"""
        # TODO use floats in [0,1.0]?
        # eg. 100 - 60
        return 100 - self.pr_yes()

  e):         """`outcome` is a boolean indicating the vote"""
        # eg. 1 - 60
        

    def cost(self, agents):
        """cost of this epistemic state given the coalition `agents`"""
        coalition else self.pr_no()cost = self.ag.join_cost if self.in_coalition else 0
        coalition_cost += self.ag.marginal_cost * self.ca coalition_cost + (ition_size
        return self.ag.join_cost) + coalition_cost


# e1 and e2 are two epistemic states
ag1_in1 = EpistemicState(ag1, 1, True)
ag1_in2 = EpistemicState(ag1, 2, True)
ag1_in3 = EpistemicState(ag1, 3, True)
ag1_in4 = EpistemicState(ag1, 4, True)
ag1_in5 = EpistemicState(ag1, 5, True)
ag1_in6 = EpistemicState(ag1, 6, True)
ag1_in7 = EpistemicState(ag1, 7, True)


"""
ag1
60% agents vote yes
            E1                              E2
max(0, 60 ((bill passed)k1)  ) - (40 ((bill not passed)k2)  )

k1:
{ag1 = yes, ag2 = yes, ag3 = yes, ag4 = yes, ag5 = yes , ag6 = yes, ag7 = yes}
{ag1 = no, ag2 = yes, ag3 = yes, ag4 = yes, ag5 = yes , ag6 = yes, ag7 = yes}

k2:
{ag1 = no, ag2 = no, ag3 = no, ag4 = no, ag5 = no , ag6 = yes, ag7 = yes}

"""

def delta_epistemic(e1, e2, outcome):
    outcome
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

# relative
def group_blame_relative(ag, e1, e2, outcome):
    return delta_epistemic * delta_cost

def group_blame_actual(ag, e1, outcome):
    c(ag, e2) * group_blame_relative

# j = number of agent (int)
# ag = subset of agents (nested dictionary)
def marginal_blame(j, ag, outcome):
    # ag_j should be a key value pair where value is a dictionary
    ag_j = 'ag' + j
    if ag_j in ag:
        # group blame - group blame without agent ag_j
        group_blame_actual(ag, e1, outcome) - group_blame(ag.pop(ag_j), e1, outcome)
    else:
        new_ag = dict(input("Enter agent info"))
        # group blame + ag_j - group blame
        group_blame_actual(ag.update(new_ag), e1, outcome) - group_blame(ag, e1, outcome)

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