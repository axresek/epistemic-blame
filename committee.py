# committee example from the paper

N = 2000 # yolo? needs to be higher than all agents costs

ag1 = { 'pr': 60, 'marginal_pr': 5, 'marginal_cost': 100, 'join_cost': 2000 }

def consrtium_cost(size, in_consortium, ag):
    size * ag.marginal_cost + (ag.join_cost if in_consortium else 0)

# TODO
#
# - define other agents
# - define other deltas
# - define marginal/group blame as functions
#
# - verify Ag = {ag_i} "group of one" blameworthiness numbers
# - verify Ag = {ag_1, ..., ag_7} "group of all" blameworthiness numbers