# pairing.py

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional


def compute_time_decay_weights(
    num_rounds: int, lambda_decay: float = 0.1
) -> np.ndarray:
    """
    Computes time decay weights using an exponential decay function.

    Parameters:
    - num_rounds (int): Number of past rounds to consider.
    - lambda_decay (float): Decay rate for the exponential function.

    Returns:
    - np.ndarray: Array of decay weights.
    """
    return np.exp(-lambda_decay * np.arange(num_rounds))


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


# for each round the pairing configuration is List[Tuple[int, int]]
# for the left out candidate, it will be (left_out_candidate_idx, -1)
# pairing_history is a dataframe with index=candidate_id,
# pairing_history.columns is growing with latest round result
# after round x, pairing_history.loc[1, "round_x"] will store the id of candidate that was paired with candidate 1 in the latest round


def update_history(
    current_round: int,
    pairings: List[Tuple[int, int]],
    previous_history: pd.DataFrame,
) -> pd.DataFrame:
    round_column = f"round_{current_round}"
    new_history = previous_history.copy()
    new_history[round_column] = 0

    for candidate1, candidate2 in pairings:
        new_history.at[candidate1, round_column] = candidate2
        if candidate2 != -1:
            new_history.at[candidate2, round_column] = candidate1
    return new_history


def calculate_pairing_energy(
    pairing_history: pd.DataFrame, decay_weights: np.ndarray
) -> pd.DataFrame:
    """
    Calculates the pairing energies based on the pairing history.

    Parameters:
    - pairing_history (pd.DataFrame): DataFrame containing pairing history.
    - decay_weights (np.ndarray): Array of decay weights.

    Returns:
    - pd.DataFrame: DataFrame of pairing energies between candidates.
    """
    pass


def calculate_left_out_energy(
    left_out_history: pd.DataFrame, decay_weights: np.ndarray
) -> pd.Series:
    """
    Calculates the left-out energies based on the left-out history.

    Parameters:
    - left_out_history (pd.DataFrame): DataFrame containing left-out history.
    - decay_weights (np.ndarray): Array of decay weights.

    Returns:
    - pd.Series: Series of left-out energies for each candidate.
    """
    pass


def generate_possible_configurations(
    candidates: List[int], num_samples: int = 1000
) -> List[Dict[str, List]]:
    """
    Generates sampled valid pairing configurations.

    Parameters:
    - candidates (List[int]): List of candidate IDs.
    - num_samples (int): Number of configurations to sample.

    Returns:
    - List[Dict[str, List]]: List of sampled configurations, each containing pairings and left-out candidates.
    """
    pass


def compute_configuration_probabilities(
    configurations: List[Dict[str, List]],
    pairing_energy: pd.DataFrame,
    left_out_energy: pd.Series,
    beta: float = 1.0,
) -> List[float]:
    """
    Computes the Boltzmann probabilities for each configuration.

    Parameters:
    - configurations (List[Dict[str, List]]): List of possible configurations.
    - pairing_energy (pd.DataFrame): DataFrame of pairing energies.
    - left_out_energy (pd.Series): Series of left-out energies.
    - beta (float): Inverse temperature parameter controlling randomness.

    Returns:
    - List[float]: List of probabilities corresponding to each configuration.
    """
    pass


def select_configuration(
    configurations: List[Dict[str, List]], probabilities: List[float]
) -> Dict[str, List]:
    """
    Selects a configuration based on computed probabilities.

    Parameters:
    - configurations (List[Dict[str, List]]): List of possible configurations.
    - probabilities (List[float]): Corresponding probabilities for each configuration.

    Returns:
    - Dict[str, List]: The chosen configuration containing pairings and left-out candidates.
    """
    pass


def run_round(
    current_round: int,
    candidates: List[int],
    pairing_history: pd.DataFrame,
    left_out_history: pd.DataFrame,
    beta: float = 1.0,
    lambda_decay: float = 0.1,
    half_life: Optional[float] = None,
    num_samples: int = 1000,
) -> Tuple[Dict[str, List], pd.DataFrame, pd.DataFrame]:
    """
    Executes a single pairing round.

    Parameters:
    - current_round (int): Current round number.
    - candidates (List[int]): List of candidate IDs.
    - pairing_history (pd.DataFrame): DataFrame containing pairing history.
    - left_out_history (pd.DataFrame): DataFrame containing left-out history.
    - beta (float): Inverse temperature parameter.
    - lambda_decay (float): Decay rate for the time decay function.
    - half_life (Optional[float]): Half-life for decay; if provided, lambda_decay is calculated from it.
    - num_samples (int): Number of configurations to sample.

    Returns:
    - Tuple[Dict[str, List], pd.DataFrame, pd.DataFrame]:
        - Selected configuration for the current round.
        - Updated pairing history DataFrame.
        - Updated left-out history DataFrame.
    """
    pass


def initialize_histories(candidates: List[int]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Initializes empty pairing and left-out histories.

    Parameters:
    - candidates (List[int]): List of candidate IDs.

    Returns:
    - Tuple[pd.DataFrame, pd.DataFrame]:
        - Empty pairing history DataFrame.
        - Empty left-out history DataFrame.
    """
    pass
