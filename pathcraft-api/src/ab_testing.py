import random
from . import models, schemas

def assign_user_to_group(experiment: models.Experiment):
    """
    Assigns a user to a group for a given experiment.
    The assignment is random, based on the weights defined in the experiment.
    """
    groups = list(experiment.groups.keys())
    weights = list(experiment.groups.values())
    return random.choices(groups, weights=weights, k=1)[0]

def get_user_group(user: models.User, experiment: models.Experiment):
    """
    Gets the group for a user for a given experiment.
    If the user is not already in a group, a new group is assigned.
    """
    if user.ab_test_group:
        return user.ab_test_group
    else:
        group = assign_user_to_group(experiment)
        user.ab_test_group = group
        return group
