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

def power_set(s):
    p = [[]]
    for x in s:
        adds = [sub + [x] for sub in p]
        p.extend(adds)
    return p    

all_coalitions = power_set(all_agents)
epis = dict()

for coalition in all_coalitions:
    epis[str(coalition)] = dict()
    c_epis = epis[str(coalition)]
    num_sure_yesvotes = 2 # 6 and 7

    for ag in coalition:
        if ag not in [6,7]:
            num_sure_yesvotes += 1
    
    print("{} has {} sure yes votes".format(coalition, num_sure_yesvotes))

    pr_yes = 0
    if num_sure_yesvotes >= 4:
        pr_yes = 1
        for agent in all_agents:
            c_epis[agent] = 1
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
            print(pr_yes)

            total_prob = 0
            # power sets of those not in coalition
            # filter possibilities eg. 1,2,3,4,5 --> [1,2,3,4] [1,3,4,5] [1,2,3,5]
            for yes in filter(lambda vs: len(vs) >= votes_needed, power_set(voters)):
                prob = 1
                for v in voters: # v = ag
                    pr_v = pr_yes[v]
                    # if ag votes no
                    if v not in yes:
                        pr_v = 1 - pr_v
                    prob = prob * pr_v
                total_prob += prob
            c_epis[pov] = total_prob
            print("Probability of yes vote: {}".format(total_prob)) # e1
        print("LOOK HERE",c_epis)
    
    # group_blame = 0
    # if num_sure_yesvotes == 7:
    #     group_blame = 0
    #     print("Group blame is ", group_blame)
    # else:
        # {2: 0.75, 3: 0.69, 4: 0.75, 5: 0.55}
        # 2: 0.25, 3: .
        # number of agents in coalition. Not in coalition = 1/7. 
        yes = num_sure_yesvotes / 7
        no = (7 - num_sure_yesvotes) / 7
        group_blame = no * pr_yes[v]

        # for ag in voters:
        #     # use each agents beliefs to set probabilities
        #     pr_yes[ag] = pr(agent_base_pr[ag] + len(coalition) * agent_factor[ag])
        # print(pr_yes)

        # total_prob = 0
        # for vs in filter(lambda vs: len(vs) >= votes_needed, power_set(voters)):
        #     prob = 1
        #     for v in voters:
        #         pr_v = pr_yes[v]
        #         if v not in vs:
        #             pr_v = 1 - pr_v
        #         prob = prob * pr_v
        #     total_prob += prob
        # print("Probability of yes vote: {}".format(total_prob))

        # why is it not printing 6 even though it's in the yes coalition and it's counting it among the votes
