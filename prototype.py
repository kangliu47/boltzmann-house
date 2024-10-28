# %%
from src.pairing import (
    random_update_pairing,
    random_update_left_out,
    create_empty_history,
    update_history_after_round,
    calculate_total_energy,
)

candidate_ids = [1, 2, 3, 4, 5, 6]
initial_pairing = [(1, 2), (3, 4), (5, 6)]
initial_history = create_empty_history(candidate_ids)
history = update_history_after_round(
    current_round=1,
    pairing_configuration=initial_pairing,
    previous_history=initial_history,
)
history = update_history_after_round(
    current_round=2,
    pairing_configuration=[(1, 3), (2, 4), (5, 6)],
    previous_history=history,
)
history = update_history_after_round(
    current_round=3,
    pairing_configuration=[(3, 5), (1, 4), (6, 2)],
    previous_history=history,
)


import numpy as np
import random

# * --- start metropolis-hasting with simulated annealing
current_round = 4
previous_history = history
print(f"History before round {current_round}")
print(history)

seed_this_round = current_round + 42
random.seed(seed_this_round)

initial_beta = 1
max_beta = 100
system_parameters = dict(
    energy_each_pair=10,
    energy_each_left_out=2,
    decay_rate_pair=0.1,
    decay_rate_left_out=0.1,
)

from src.pairing import (
    check_for_new_candidates,
    add_new_candidates_to_history,
    get_candidate_ids,
)

# active_configuration = [(3, 5), (1, 4), (6, 2), (7, -1)] # add one more
# active_configuration = [(3, 5), (1, 4), (6, 2), (7, 8)]  # add two more
# active_configuration = [(3, 5), (1, 4), (6, 2), (7, 8), (9, -1)]  # add three more
# active_configuration = [(3, 5), (1, 4), (6, -1)]  # remove one
active_configuration = [
    (3, 5),
    (1, 4),
    (6, -1),
    (9, 10),
    (7, 8),
]  # remove one and add a few
new_candidates = check_for_new_candidates(candidate_ids, active_configuration)
current_candidates = get_candidate_ids(active_configuration)

print(f"\nPrevious Candidates = {candidate_ids}")
print(f"Current Candidates = {current_candidates}")
print(f"New Candidates = {new_candidates}")

previous_history = add_new_candidates_to_history(previous_history, new_candidates)

active_energy = calculate_total_energy(
    current_round, active_configuration, previous_history, **system_parameters
)
beta = initial_beta

print(f"\nStart Simulation:")
for step in range(10):
    new_configuration = random_update_pairing(active_configuration, seed_this_round)
    new_configuration = random_update_left_out(new_configuration, seed_this_round)
    new_energy = calculate_total_energy(
        current_round, new_configuration, previous_history, **system_parameters
    )
    delta_energy = new_energy - active_energy
    acceptance_prob = min(1, np.exp(-beta * delta_energy))
    random_number = random.random()
    print(
        f"Step={step}, Beta={beta}, {active_configuration} with energy {active_energy}"
    )
    if random_number < acceptance_prob:
        active_configuration = new_configuration
        active_energy = new_energy
        print("Accept Update!")

    beta = min(beta * 1.2, max_beta)


new_history = update_history_after_round(
    current_round, active_configuration, previous_history
)
print(new_history)
