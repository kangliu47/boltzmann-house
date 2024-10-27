# pairing.py

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional


def get_round_name(round_idx: int) -> str:
    return f"round_{round_idx}"


def compute_time_decay_weights(num_rounds: int, decay_rate: float = 0.1) -> pd.Series:
    weight_values = np.exp(-decay_rate * np.arange(num_rounds))
    time_index = [get_round_name(round_idx) for round_idx in np.arange(num_rounds)]
    return pd.Series(weight_values, index=time_index)


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


def update_history(
    current_round: int,
    pairings: List[Tuple[int, int]],
    previous_history: pd.DataFrame,
) -> pd.DataFrame:
    # NOTE: We assumes that the left_out candidate will be pair with -1
    round_column = get_round_name(current_round)
    new_history = previous_history.copy()
    new_history[round_column] = 0

    for candidate1, candidate2 in pairings:
        new_history.at[candidate1, round_column] = candidate2
        if candidate2 != -1:
            new_history.at[candidate2, round_column] = candidate1
    return new_history


def calculate_total_energy(
    current_round: int,
    pairings: List[Tuple[int, int]],
    previous_history: pd.DataFrame,
    energy_each_pair: float,
    energy_left_out: float,
) -> float:
    total_energy = 0
    number_of_past_rounds = current_round - 1
    assert previous_history.shape[1] == number_of_past_rounds
    pair_weights_decay = compute_time_decay_weights(num_rounds=number_of_past_rounds)
    for new_pair in pairings:
        if any(new_pair) == -1:
            energy_this_pair = 0 * energy_left_out
        else:
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
        history_for_1 = pairing_history.loc[candidate_1]
        paired_with_2 = (history_for_1 == candidate_2).astype(int)
        return paired_with_2


def calculate_pairing_energy(
    historical_pairing: pd.Series,
    decay_weights: pd.Series,
) -> float:
    assert historical_pairing.index.equals(decay_weights.index)
    overlap_weights = historical_pairing * decay_weights
    return overlap_weights.sum()


# * --------- coding ends here -----2024-10-26----
def calculate_left_out_energy(
    pairings: List[Tuple[int, int]],
    pairing_history: pd.DataFrame,
    decay_weights: np.ndarray,
) -> pd.Series:
    pass


def generate_possible_pairing_configurations(
    candidates: List[int],
):
    pass


def compute_configuration_probabilities(
    configurations: List[Dict[str, List]],
    pairing_energy: pd.DataFrame,
    left_out_energy: pd.Series,
    beta: float = 1.0,
) -> List[float]:
    pass


def select_configuration(
    configurations: List[Dict[str, List]], probabilities: List[float]
) -> Dict[str, List]:
    pass


def run_round(
    current_round: int,
    candidates: List[int],
    pairing_history: pd.DataFrame,
    left_out_history: pd.DataFrame,
    beta: float = 1.0,
    decay_rate: float = 0.1,
    half_life: Optional[float] = None,
    num_samples: int = 1000,
) -> Tuple[Dict[str, List], pd.DataFrame, pd.DataFrame]:
    pass


def initialize_histories(candidates: List[int]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    pass
