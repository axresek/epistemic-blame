def pr(n):
    return min(max(n, 0), 1)

all_agents = [1,2,3,4,5,6,7]

# n x factor is the boosted probability
agent_base_pr = dict()
agent_base_pr[1] = 0.6
agent_base_pr[2] = 0.6
agent_base_pr[3] = 0.6
agent_base_pr[4] = 0.6
agent_base_pr[5] = 0.4
agent_base_pr[6] = 0.6
agent_base_pr[7] = 0.6

agent_factor = dict()
agent_factor[1] = 0.05
agent_factor[2] = 0.05
agent_factor[3] = 0.03
agent_factor[4] = 0.05
agent_factor[5] = 0.05
agent_factor[6] = 0.05
agent_factor[7] = 0.05

# if they were IN the coalition this is the cost to switch:
agent_switch_cost = dict()
agent_switch_cost[1] = 2000
agent_switch_cost[2] = 500
agent_switch_cost[3] = 2000
agent_switch_cost[4] = 2000
agent_switch_cost[5] = 2000
agent_switch_cost[6] = 0
agent_switch_cost[7] = 0

def power_set(s):
    p = [[]]
    for x in s:
        adds = [sub + [x] for sub in p]
        p.extend(adds)
    return p    

all_coalitions = power_set(all_agents)
epis = dict()

cost_dict = dict()

for coalition in all_coalitions:
    epis[str(coalition)] = dict()
    # epistemic states for everyone in the coalition
    # c = coalition
    c_epis = epis[str(coalition)]
    num_sure_yesvotes = 2 # 6 and 7

    for ag in coalition:
        if ag not in [6,7]:
            num_sure_yesvotes += 1
    
    # print("{} has {} sure yes votes".format(coalition, num_sure_yesvotes))

    pr_yes = 0
    if num_sure_yesvotes >= 4:
        pr_yes = 1
        for agent in all_agents:
            c_epis[agent] = 1 # probability of voting yes
    else:  
        votes_needed = 4 - num_sure_yesvotes
        # now, compute probability we get votes_needed out of ag1 through 5
        # voters = those not in coalition
        voters = list(filter(lambda ag: ag not in coalition and ag not in [6,7], all_agents))

        # map from coalition to a {map from agents to probabilities}
        # pov = one agent's epistemic state
        for pov in all_agents:


            pr_yes = dict()
            for ag in voters:

                # use each agents beliefs to set probabilities
                # using epistemic state (pov) of each agent to apply to all agents
                pr_yes[ag] = pr(agent_base_pr[pov] + len(coalition) * agent_factor[pov])
            # print("probabilities for yes: ", pr_yes)
            
            pr_no = dict()
            # key is ag, val is probability
            for key, val in pr_yes.items():
                val = 1 - val
                pr_no[key] = val
            # print("probabilities for no: ", pr_no)

            total_prob = 0
            """ PROBABILITY OF YES """
            # power sets of those not in coalition
            # filter possibilities eg. 1,2,3,4,5 --> [1,2,3,4] [1,3,4,5] [1,2,3,5]
        #     for yes in filter(lambda vs: len(vs) >= votes_needed, power_set(voters)):
        #         prob = 1
        #         for v in voters: # v = ag
        #             pr_v = pr_yes[v]
        #             # if ag votes no
        #             if v not in yes:
        #                 pr_v = 1 - pr_v
        #             prob = prob * pr_v
        #         total_prob += prob
        #     c_epis[pov] = total_prob
        #     print("Probability of yes vote: {}".format(total_prob)) # e1
        # print("LOOK HERE",c_epis)
            """ PROBABILITY OF A NO VOTE 
                using world where bill doesn't pass """
            # voters are those not in the coalition or not 6 or 7 that could vote yes or no
            for no in filter(lambda vs: len(vs) >= 4, power_set(voters)):
                # print(no) # prints out agents not in coalition, when vote is no
                prob = 1
                for v in voters: # v = ag
                    pr_v = pr_no[v]

                    # new info: for cost
                    # save all the times ag is not in coalition

                    # if ag votes yes
                    if v not in no:
                        pr_v = 1 - pr_v
                        
                        # new info: for cost
                        # save all the times ag is in the coalition
                    
                    prob = prob * pr_v
                total_prob += prob
            c_epis[pov] = total_prob #
            # print("Agent {} Probability of no vote: {}".format(pov, total_prob))
        print("LOOK HERE",c_epis) # map from agents to their beliefs that it'll be a no vote


# particular coalition and agent's perspective
# where they're part of the coalition or they're not
# ag1 in coalition or not in the coalition and then look at the outcome of bill not passing
# E2 is every other possible world from that agent's perspective
# have to go through every possible coalition and look at what agent believes in that circumstance

# cost function that can take a set of agents and tell you have expensive th

""" COST """
# N = 200
# (N - Max (cost(ag, e2) - c(ag, e1))) / N # lower bound at 0

# go through each powerset
# save c_epis outputs for each agent

# If there is more than one way for the agents in Ag to bring about E, 
# we can think of c(Ag, E) as being the cost of the cheapest way to do so

# calc group blame, for each agents epistemic state blame for group and blame for agent
# pg. 5: db definition, for individual blame
# pg. 4 definition of gb, generate group blame of whole group . 2nd gb is definied in terms of the first


# define delta (epistemic state), tuple with 2 things in it agent number and coalition
# map coalitions to probabilities
# epis, agent number, coaltion, agent number, and coalition
# 2 epistemic states (ie 2 agents' beliefs on coalitions), given outcome is a no vote
def delta(epis, ag1, col1, ag2, col2):
   return max(0, epis[col1][ag1] - epis[col2][ag2])

# cost
# cost of bringing about epistemic state (ie coalitions), also cost of yes vote for agents
N = 200 # balance parameter
def cost(ag, e):
    

def cost_balanced(ag1, e1, ag2, e2):
    return (N - max(cost(ag1, e1) - cost(ag2, e2), 0)) / N

# define 4-arg gb (needs delta and cost)
# calculates group blameworthiness of group ag with epistemic state e1 relative to epistemic state e2
def four_arg_gb(delta, cost_balanced):
    return delta * cost_balanced

