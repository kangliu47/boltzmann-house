# pairing.py

import numpy as np
import pandas as pd
import math
import random
import itertools
from typing import List, Tuple, Dict, Optional


# * ------ data utilities ------
def get_round_name(round_idx: int) -> str:
    return f"round_{round_idx}"


def compute_time_decay_weights(num_rounds: int, decay_rate: float) -> pd.Series:
    weight_values = np.exp(-decay_rate * np.arange(num_rounds))
    time_index = [
        get_round_name(num_rounds - round_idx) for round_idx in np.arange(num_rounds)
    ]
    return pd.Series(weight_values, index=time_index).sort_index(ascending=True)


def create_empty_history(candidate_ids: list) -> pd.DataFrame:
    return pd.DataFrame({}, index=candidate_ids)


def add_candidate(candidate_ids: list, new_candidate_id: int) -> list:
    if new_candidate_id not in candidate_ids:
        candidate_ids.append(new_candidate_id)
    return candidate_ids


def remove_candidate(candidate_ids: list, candidate_id: int) -> list:
    if candidate_id in candidate_ids:
        candidate_ids.remove(candidate_id)
    else:
        raise ValueError(f"Candidate ID {candidate_id} not found in the list.")
    return candidate_ids


def update_history_after_round(
    current_round: int,
    pairing_configuration: List[Tuple[int, int]],
    previous_history: pd.DataFrame,
) -> pd.DataFrame:
    # NOTE: We assumes that the left_out candidate will be pair with -1
    round_column = get_round_name(current_round)
    new_history = previous_history.copy()
    new_history[round_column] = 0

    for candidate1, candidate2 in pairing_configuration:
        new_history.at[candidate1, round_column] = candidate2
        if candidate2 != -1:
            new_history.at[candidate2, round_column] = candidate1
    return new_history


def check_for_new_candidates(
    candidate_ids: List[int],
    pairing_configuration: List[tuple],
) -> list:
    current_candidates = get_candidate_ids(pairing_configuration)
    return list(set(current_candidates) - set(candidate_ids))


def get_candidate_ids(pairing_configuration: List[tuple]) -> list:
    candidate_ids = set()
    for pair in pairing_configuration:
        candidate_ids.update(pair)
    return [x for x in candidate_ids if x != -1]


def add_new_candidates_to_history(
    previous_history: pd.DataFrame, new_candidates: list
) -> pd.DataFrame:
    # Identify new candidates and add rows for them
    new_history = previous_history.copy()
    for candidate in new_candidates:
        new_history.loc[candidate] = 0
    return new_history


# * ------ energy calculation ------
def calculate_total_energy(
    current_round: int,
    pairing_configuration: List[Tuple[int, int]],
    previous_history: pd.DataFrame,
    energy_each_pair: float,
    energy_each_left_out: float,
    decay_rate_pair: float = 0.1,
    decay_rate_left_out: float = 0.1,
) -> float:
    total_pairing_energy = calculate_total_pairing_energy(
        current_round,
        pairing_configuration,
        previous_history,
        energy_each_pair,
        decay_rate_pair,
    )
    total_left_out_energy = calculate_total_left_out_energy(
        current_round,
        pairing_configuration,
        previous_history,
        energy_each_left_out,
        decay_rate_left_out,
    )
    return total_pairing_energy + total_left_out_energy


def calculate_total_pairing_energy(
    current_round: int,
    pairing_configuration: List[Tuple[int, int]],
    previous_history: pd.DataFrame,
    energy_each_pair: float,
    decay_rate_pair: float = 0.1,
) -> float:
    total_energy = 0
    number_of_past_rounds = current_round - 1
    assert previous_history.shape[1] == number_of_past_rounds
    pair_weights_decay = compute_time_decay_weights(
        num_rounds=number_of_past_rounds, decay_rate=decay_rate_pair
    )
    full_pairs = get_all_full_pairs(pairing_configuration)
    for new_pair in full_pairs:
        historical_pairing = find_historical_pairing(new_pair, previous_history)
        energy_this_pair = energy_each_pair * calculate_pairing_energy(
            historical_pairing, pair_weights_decay
        )
        total_energy += energy_this_pair
    return total_energy


def find_historical_pairing(
    new_pair: Tuple[int, int], pairing_history: pd.DataFrame
) -> pd.Series:
    # return the series with index=round_{idx} and each cell = 1 or 0 depending on if the new_pair previously are in history
    candidate_1, candidate_2 = new_pair
    if candidate_1 == -1 or candidate_2 == -1:
        raise ValueError("Invalid Pairing!")
    else:
        history_for_1 = pairing_history.loc[candidate_1].copy()
        paired_with_2 = (history_for_1 == candidate_2).astype(int)
        return paired_with_2


def calculate_pairing_energy(
    historical_pairing: pd.Series,
    decay_weights: pd.Series,
) -> float:
    # assert historical_pairing.index.equals(decay_weights.index)
    overlap_weights = historical_pairing * decay_weights
    return overlap_weights.sum()


def calculate_total_left_out_energy(
    current_round: int,
    pairing_configuration: List[Tuple[int, int]],
    previous_history: pd.DataFrame,
    energy_each_left_out: float,
    decay_rate_left_out: float = 0.1,
) -> float:
    number_of_past_rounds = current_round - 1
    assert previous_history.shape[1] == number_of_past_rounds
    left_out_decay_weights = compute_time_decay_weights(
        num_rounds=number_of_past_rounds, decay_rate=decay_rate_left_out
    )
    left_out_candidate = get_left_out_candidate(pairing_configuration)
    if left_out_candidate == -1:
        left_out_energy = 0
    else:
        left_out_history = find_historical_left_out(
            left_out_candidate, previous_history
        )
        left_out_energy = (left_out_history * left_out_decay_weights).sum()
    return left_out_energy * energy_each_left_out


def find_historical_left_out(
    candidate_id: int,
    pairing_history: pd.DataFrame,
) -> pd.Series:
    assert (
        candidate_id in pairing_history.index
    ), f"Candidate {candidate_id} not in pairing history"
    candidate_row = pairing_history.loc[candidate_id]
    left_out_series = candidate_row.apply(lambda x: 1 if x == -1 else 0)
    return left_out_series


def get_left_out_candidate(
    pairing_configuration: List[Tuple[int, int]],
) -> int:
    left_out_pairs = get_left_out_pairs(pairing_configuration)
    if len(left_out_pairs) > 0:
        a, b = left_out_pairs[0]
        if b == -1:
            return a
        elif a == -1:
            return b
    return -1


# * ------ sample configurations ------
def create_random_pairing_configuration(candidates: list, seed: int) -> List[tuple]:
    candidates_copy = candidates.copy()
    if len(candidates_copy) % 2 != 0:
        candidates_copy.append(-1)
    random.seed(seed)
    random.shuffle(candidates_copy)
    pairing_configuration = list(itertools.zip_longest(*[iter(candidates_copy)] * 2))
    return pairing_configuration


def random_update_pairing(
    pairing_configuration: List[Tuple[int, int]], seed: int
) -> List[tuple]:
    full_pairs = get_all_full_pairs(pairing_configuration)
    random.seed(seed)
    pair_1, pair_2 = random.sample(full_pairs, 2)
    return update_pairing(pairing_configuration, pair_1, pair_2)


def random_update_left_out(
    pairing_configuration: List[Tuple[int, int]], seed: int
) -> List[tuple]:
    full_pairs = get_all_full_pairs(pairing_configuration)
    left_pairs = get_left_out_pairs(pairing_configuration)
    if len(left_pairs) == 0:
        return pairing_configuration
    else:
        random.seed(seed)
        valid_pair = random.choice(full_pairs)
        left_pair = left_pairs[0]
        return update_pairing(
            pairing_configuration, pair_1=valid_pair, pair_2=left_pair
        )


def update_pairing(
    pairing_configuration: List[tuple], pair_1: tuple, pair_2: tuple
) -> List[tuple]:
    new_configuration = pairing_configuration.copy()
    new_configuration.remove(pair_1)
    new_configuration.remove(pair_2)
    new_pair_1, new_pair_2 = regroup_pairing(pair_1, pair_2)
    new_configuration.append(new_pair_1)
    new_configuration.append(new_pair_2)
    return new_configuration


def get_left_out_pairs(pairing_configuration: List[Tuple]) -> list:
    left_out_pairs = [x for x in pairing_configuration if -1 in x]
    return left_out_pairs


def get_all_full_pairs(pairing_configuration: List[tuple]) -> List[tuple]:
    full_pairs = [x for x in pairing_configuration if -1 not in x]
    return full_pairs


def regroup_pairing(pair_1: tuple, pair_2: tuple) -> Tuple[tuple, tuple]:
    # NOTE: this is assuming there are no order in each pair
    a, b = pair_1
    c, d = pair_2
    return (a, c), (b, d)


def calculate_total_configurations(n_candidates: int) -> int:
    if n_candidates % 2 == 0:
        p = n_candidates // 2
    else:
        p = (n_candidates - 1) // 2
    numerator = math.factorial(n_candidates)
    denominator = math.factorial(p) * (2**p)
    return numerator // denominator


def run_round_with_metropolis(
    next_round: int,
    current_candidates: List[int],
    pairing_history: pd.DataFrame,
    n_steps: int,
    seed: int,
) -> List[tuple]:
    pass
