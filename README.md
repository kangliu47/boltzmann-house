# boltzmann-house

Step into BoltzmannHouse, where every cup and every conversation is a fresh discovery governed by the elegant laws of physics.

---

## Pairing History

The pairing history is a Pandas DataFrame that records the pairings of candidates over multiple rounds. It is structured as follows:

- **Index**: Candidate IDs.
- **Columns**: Round identifiers (round_1, round_2, etc.), with the most recent round on the left.
- **Cell Values**:
  - The ID of the candidate that the current candidate was paired with in that round.
  - `-1` if the candidate was left out in that round.

### Example

Consider 5 candidates participating in two rounds of pairings:

#### Round 1:

- Pairings: (1, 2), (3, 4)
- Left out: 5

#### Round 2:

- Pairings: (1, 3), (2, 5)
- Left out: 4

The pairing history DataFrame after these rounds is:

| Candidate ID | round_2 | round_1 |
| ------------ | ------- | ------- |
| 1            | 3       | 2       |
| 2            | 5       | 1       |
| 3            | 1       | 4       |
| 4            | -1      | 3       |
| 5            | 2       | -1      |

#### Explanation:

**Round 1 (round_1)**:

- Candidate 1 was paired with 2.
- Candidate 2 was paired with 1.
- Candidate 3 was paired with 4.
- Candidate 4 was paired with 3.
- Candidate 5 was left out (`-1`).

**Round 2 (round_2)**:

- Candidate 1 was paired with 3.
- Candidate 3 was paired with 1.
- Candidate 2 was paired with 5.
- Candidate 5 was paired with 2.
- Candidate 4 was left out (`-1`).

This data structure allows for efficient tracking and analysis of each candidate's pairing history across rounds. It provides a clear view of past interactions, which is essential for algorithms that aim to minimize repeats and ensure fair distribution in future pairings.
