import pytest
import numpy as np
import pandas as pd
from src.pairing import update_history

from src.pairing import (
    get_round_name,
    compute_time_decay_weights,
    create_empty_history,
    add_candidate,
    remove_candidate,
    find_historical_pairing,
    calculate_pairing_energy,
)


def test_get_round_name():
    round_idx = 1
    expected_round_name = "round_1"
    assert get_round_name(round_idx) == expected_round_name


def test_compute_time_decay_weights():
    num_rounds = 5
    lambda_decay = 0.1
    expected_weights = np.exp(-lambda_decay * np.arange(num_rounds))
    weights = compute_time_decay_weights(num_rounds, lambda_decay)
    assert isinstance(weights, pd.Series)
    assert np.allclose(weights, expected_weights)


def test_create_empty_history():
    candidate_ids = [1, 2, 3]
    history = create_empty_history(candidate_ids)
    expected_history = pd.DataFrame({}, index=candidate_ids)
    pd.testing.assert_frame_equal(history, expected_history)


def test_add_candidate():
    candidate_ids = [1, 2, 3]
    new_candidate = 4
    updated_candidate_ids = add_candidate(candidate_ids, new_candidate)
    expected_candidate_ids = [1, 2, 3, 4]
    assert updated_candidate_ids == expected_candidate_ids


def test_remove_candidate_existing():
    candidate_ids = [1, 2, 3, 4]
    candidate_to_remove = 3
    updated_candidate_ids = remove_candidate(candidate_ids, candidate_to_remove)
    expected_candidate_ids = [1, 2, 4]
    assert updated_candidate_ids == expected_candidate_ids


def test_update_history_first_round():
    current_round = 1
    pairings = [(1, 2), (3, 4), (5, -1)]
    candidate_ids = [1, 2, 3, 4, 5]
    previous_history = create_empty_history(candidate_ids)
    updated_history = update_history(current_round, pairings, previous_history)
    expected_history = create_empty_history(candidate_ids)
    expected_history["round_1"] = [2, 1, 4, 3, -1]
    pd.testing.assert_frame_equal(updated_history, expected_history)


def test_update_history_second_round():
    first_round_pairings = [(1, 2), (3, 4), (5, -1)]
    second_round_pairings = [(1, 3), (2, 5), (4, -1)]
    candidate_ids = [1, 2, 3, 4, 5]
    initial_condition = create_empty_history(candidate_ids)
    after_first_round = update_history(1, first_round_pairings, initial_condition)
    after_second_round = update_history(2, second_round_pairings, after_first_round)
    expected_history = initial_condition.copy()
    expected_history["round_1"] = [2, 1, 4, 3, -1]
    expected_history["round_2"] = [3, 5, 1, -1, 2]
    pd.testing.assert_frame_equal(after_second_round, expected_history)


def test_find_historical_pairing():
    candidate_ids = [1, 2, 3, 4, 5]
    initial_condition = create_empty_history(candidate_ids)
    first_round_pairings = [(1, 3), (2, 4), (5, -1)]
    second_round_pairings = [(1, 2), (3, 5), (4, -1)]
    after_first_round = update_history(1, first_round_pairings, initial_condition)
    after_second_round = update_history(2, second_round_pairings, after_first_round)

    historical_pairing = find_historical_pairing((1, 3), after_second_round)
    expected_series = pd.Series(
        {
            get_round_name(1): 1,
            get_round_name(2): 0,
        },
        name=historical_pairing.name,
    )
    pd.testing.assert_series_equal(historical_pairing, expected_series)


def test_find_historical_pairing_not_existing():
    candidate_ids = [1, 2, 3, 4, 5]
    initial_condition = create_empty_history(candidate_ids)
    first_round_pairings = [(1, 3), (2, 4), (5, -1)]
    second_round_pairings = [(1, 2), (3, 5), (4, -1)]
    after_first_round = update_history(1, first_round_pairings, initial_condition)
    after_second_round = update_history(2, second_round_pairings, after_first_round)

    historical_pairing = find_historical_pairing((1, 5), after_second_round)
    expected_series = pd.Series(
        {
            get_round_name(1): 0,
            get_round_name(2): 0,
        },
        name=historical_pairing.name,
    )
    pd.testing.assert_series_equal(historical_pairing, expected_series)


def test_find_historical_pairing_invalid():
    candidate_ids = [1, 2, 3, 4, 5]
    initial_condition = create_empty_history(candidate_ids)
    with pytest.raises(ValueError):
        _ = find_historical_pairing((1, -1), initial_condition)


def test_calculate_pairing_energy():
    historical_pairing = pd.Series(
        {
            get_round_name(1): 1,
            get_round_name(2): 0,
        },
    )
    decay_weights = pd.Series(
        {
            get_round_name(1): 0.55,
            get_round_name(2): 1,
        },
    )
    results = calculate_pairing_energy(historical_pairing, decay_weights)
    assert results == 0.55
