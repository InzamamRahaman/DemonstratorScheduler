import numpy as np

def fitness(assignments, costs, qualifications, seniority,
            time_per_lab, time_limits,
            demonstrator_requirements, qualification_violation_factor,
            seniority_bonus_factor, time_limit_violation_factor,
            demonstrator_violation_factor):
    """
    Given an assignment of demonstrators to labs and various constants that
    describe the current requirements, compute a cost for that particular assignment
    :param assignments: a binary matrix of size D x L that describes the current assignment of
                        demonstrators to labs. If assignment[d][l] = 1, then demonstrator d is
                        assigned to lab l else d is NOT assigned to lab l. This is what
                        we are trying to optimize over
    :param costs: a matrix of size L x L that describes the cost of assigning
                  any arbitrary demonstrator to any two labs.
                  if costs[l1][l2] = 0, then there is no penalty to co-assignment
                  if costs[l1][l2] < 0, then we want to ENCOURAGE a demonstrator
                                        to be assignment to both lab l1 and l2
                  if costs[l1][l2] > 0, then we want to prevent, as much as possible,
                                        the assignment of a demonstrator to both
                                        l1 and l2

    :param qualifications: a binary matrix of size D x L that simply indicates if
                           a demonstrator is qualified to demonstrate for a lab
                           if qualifications[d][l] = 1, then d is qualified for l
                           if qualifications[d][l] = 0, then d is NOT qualified for l
    :param seniority: a matrix of size D x L that describes the degree of preference
                      to assigning a particular demonstrator to a particular lab
    :param time_per_lab: a vector of size L describing the number of hours
                         taken by a particular lab
    :param time_limits: a vector of size D describing the number of hours that
                        can be worked by a demonstrator in a 2 week cycle
    :param demonstrator_requirements: a vector of size L describing the number
                                      of demonstrators required for each lab
    :param qualification_violation_factor:
    :param seniority_bonus_factor:
    :param time_limit_violation_factor:
    :param demonstrator_violation_factor:
    :return: the cost of an assignment
    """

    num_demonstrators, num_labs = assignments.shape


    co_assignment_cost = 0
    qualification_violation_cost = 0
    time_violation_cost = 0
    demonstrator_requirement_costs = 0

    seniority_bonus = 0

    for d in range(num_demonstrators):
        for l1 in range(num_labs):
            for l2 in range(num_labs):
                if l1 != l2:
                    cost = assignments[d][l1] * assignments[d][l2] * costs[l1][l2]
                    co_assignment_cost += cost

    demonstrator_counts = np.zeros_like(demonstrator_requirements)
    time_per_demonstrator = np.zeros_like(time_limits)
    for d in range(num_demonstrators):
        for l in range(num_labs):
            d_assigned_to_l = assignments[d][l]
            time_per_demonstrator[d] += time_per_lab[l] * d_assigned_to_l
            demonstrator_counts[l] += d_assigned_to_l
            qualification_violation_cost += (1 - qualifications[d][l]) * d_assigned_to_l
            seniority_bonus = seniority[d][l] * d_assigned_to_l

    time_violation_cost = np.sum(np.abs(time_per_demonstrator - time_limits))
    time_violation_cost *= time_limit_violation_factor

    demonstrator_requirement_costs = np.sum(np.abs(demonstrator_counts - demonstrator_requirements))
    demonstrator_requirement_costs *= demonstrator_violation_factor

    qualification_violation_cost *= qualification_violation_factor
    seniority_bonus *= seniority_bonus_factor

    overall_cost = co_assignment_cost + qualification_violation_cost + \
        time_violation_cost + demonstrator_requirement_costs

    overall_bonus = seniority_bonus

    cost_func_value = overall_cost - overall_bonus

    return cost_func_value


def fitness_func_generator(costs, qualifications, seniority,
            time_per_lab, time_limits,
            demonstrator_requirements, qualification_violation_factor,
            seniority_bonus_factor, time_limit_violation_factor,
            demonstrator_violation_factor):
    """
    Generates a fitness function particular to a set of constants
    :param costs: a matrix of size L x L that describes the cost of assigning
                  any arbitrary demonstrator to any two labs.
                  if costs[l1][l2] = 0, then there is no penalty to co-assignment
                  if costs[l1][l2] < 0, then we want to ENCOURAGE a demonstrator
                                        to be assignment to both lab l1 and l2
                  if costs[l1][l2] > 0, then we want to prevent, as much as possible,
                                        the assignment of a demonstrator to both
                                        l1 and l2

    :param qualifications: a binary matrix of size D x L that simply indicates if
                           a demonstrator is qualified to demonstrate for a lab
                           if qualifications[d][l] = 1, then d is qualified for l
                           if qualifications[d][l] = 0, then d is NOT qualified for l
    :param seniority: a matrix of size D x L that describes the degree of preference
                      to assigning a particular demonstrator to a particular lab
    :param time_per_lab: a vector of size L describing the number of hours
                         taken by a particular lab
    :param time_limits: a vector of size D describing the number of hours that
                        can be worked by a demonstrator in a 2 week cycle
    :param demonstrator_requirements: a vector of size L describing the number
                                      of demonstrators required for each lab
    :param qualification_violation_factor:
    :param seniority_bonus_factor:
    :param time_limit_violation_factor:
    :param demonstrator_violation_factor:
    :return function that accepts a matrix of assignments to compute the fitness
    """
    def f(assignment):
        cost = fitness(assignment, costs, qualifications, seniority,
            time_per_lab, time_limits,
            demonstrator_requirements, qualification_violation_factor,
            seniority_bonus_factor, time_limit_violation_factor,
            demonstrator_violation_factor)
        return cost
    return f


