import pytest
import numpy as np
import pandas as pd
from src.pairing import update_history_after_round

from src.pairing import (
    get_round_name,
    compute_time_decay_weights,
    create_empty_history,
    add_candidate,
    remove_candidate,
    find_historical_pairing,
    calculate_pairing_energy,
    get_left_out_candidate,
    find_historical_left_out,
    create_random_pairing_configuration,
    random_update_pairing,
    random_update_left_out,
    calculate_total_configurations,
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
    assert np.allclose(weights.sort_values(ascending=False), expected_weights)


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
    updated_history = update_history_after_round(current_round, pairings, previous_history)
    expected_history = create_empty_history(candidate_ids)
    expected_history["round_1"] = [2, 1, 4, 3, -1]
    pd.testing.assert_frame_equal(updated_history, expected_history)


def test_update_history_second_round():
    first_round_pairings = [(1, 2), (3, 4), (5, -1)]
    second_round_pairings = [(1, 3), (2, 5), (4, -1)]
    candidate_ids = [1, 2, 3, 4, 5]
    initial_condition = create_empty_history(candidate_ids)
    after_first_round = update_history_after_round(1, first_round_pairings, initial_condition)
    after_second_round = update_history_after_round(2, second_round_pairings, after_first_round)
    expected_history = initial_condition.copy()
    expected_history["round_1"] = [2, 1, 4, 3, -1]
    expected_history["round_2"] = [3, 5, 1, -1, 2]
    pd.testing.assert_frame_equal(after_second_round, expected_history)


def test_find_historical_pairing():
    candidate_ids = [1, 2, 3, 4, 5]
    initial_condition = create_empty_history(candidate_ids)
    first_round_pairings = [(1, 3), (2, 4), (5, -1)]
    second_round_pairings = [(1, 2), (3, 5), (4, -1)]
    after_first_round = update_history_after_round(1, first_round_pairings, initial_condition)
    after_second_round = update_history_after_round(2, second_round_pairings, after_first_round)

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
    after_first_round = update_history_after_round(1, first_round_pairings, initial_condition)
    after_second_round = update_history_after_round(2, second_round_pairings, after_first_round)

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


def test_get_left_out_candidate_left_out_exists():
    pairings = [(1, 2), (3, -1)]
    result = get_left_out_candidate(pairings)
    assert result == 3


def test_get_left_out_candidate_no_left_out():
    pairings = [(1, 2), (3, 4)]
    result = get_left_out_candidate(pairings)
    assert result == -1


def test_get_left_out_candidate_empty_list():
    pairings = []
    result = get_left_out_candidate(pairings)
    assert result == -1


def test_find_historical_left_out():
    candidates = [1, 2, 3, 4, 5]
    rounds = ["round_3", "round_2", "round_1"]  # Most recent round first
    data = {
        "round_3": {1: 5, 2: 3, 3: 2, 4: -1, 5: 1},
        "round_2": {1: 2, 2: 1, 3: 4, 4: 3, 5: -1},
        "round_1": {1: 3, 2: -1, 3: 1, 4: 5, 5: 4},
    }
    pairing_history = pd.DataFrame(data, index=candidates, columns=rounds)
    # Expected left-out history for candidate 5
    expected_series_5 = pd.Series(
        [0, 1, 0],
        index=rounds,
        name=5,
    )
    result_series_5 = find_historical_left_out(5, pairing_history)
    pd.testing.assert_series_equal(result_series_5, expected_series_5)
    expected_series_1 = pd.Series(
        [0, 0, 0],
        index=rounds,
        name=1,
    )
    result_series_1 = find_historical_left_out(1, pairing_history)
    pd.testing.assert_series_equal(result_series_1, expected_series_1)


def test_create_random_pairing():
    results = create_random_pairing_configuration(candidates=[1, 2, 3, 4, 5], seed=42)
    assert results == [(4, 2), (3, 5), (1, -1)]


def test_random_update_paring():
    initial_pairing = [(1, 2), (3, 4), (5, 6)]
    results = random_update_pairing(initial_pairing, seed=42)
    assert results == [(3, 4), (5, 1), (6, 2)]


def test_random_update_left_out():
    without_left_out = [(1, 2), (3, 4), (5, 6)]
    assert without_left_out == random_update_left_out(without_left_out, seed=42)
    initial_pairing = [(1, 2), (3, 4), (5, -1)]
    results = random_update_left_out(initial_pairing, seed=42)
    assert results == [(3, 4), (1, 5), (2, -1)]


def test_calculate_total_configurations():
    assert calculate_total_configurations(3) == 3
    assert calculate_total_configurations(4) == 3
    assert calculate_total_configurations(5) == 15
    assert calculate_total_configurations(6) == 15
    assert calculate_total_configurations(7) == 105
    assert calculate_total_configurations(8) == 105
