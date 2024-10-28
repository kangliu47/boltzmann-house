# Example Output from Simulated Annealing




## History before round 4

| round_1 | round_2 | round_3 |
| ------- | ------- | ------- |
| 2       | 3       | 4       |
| 1       | 4       | 6       |
| 4       | 1       | 5       |
| 3       | 2       | 1       |
| 6       | 6       | 3       |
| 5       | 5       | 2       |

**Previous Candidates:** [1, 2, 3, 4, 5, 6]  
**Current Candidates:** [1, 3, 4, 5, 6, 7, 8, 9, 10]  
**New Candidates:** [8, 9, 10, 7]

### Start Simulation:

```bash
Step=0, Beta=1, [(3, 5), (1, 4), (6, -1), (9, 10), (7, 8)] with energy 20.0
Accept Update!
Step=1, Beta=1.2, [(7, 8), (3, 1), (5, 4), (9, 6), (10, -1)] with energy 9.048374180359595
Accept Update!
Step=2, Beta=1.44, [(9, 6), (7, 3), (8, 1), (5, 10), (4, -1)] with energy 0.0
Accept Update!
Step=3, Beta=1.728, [(5, 10), (9, 7), (6, 3), (8, 4), (1, -1)] with energy 0.0
Accept Update!
Step=4, Beta=2.0736, [(8, 4), (5, 9), (10, 7), (6, 1), (3, -1)] with energy 0.0
Accept Update!
Step=5, Beta=2.48832, [(6, 1), (8, 5), (4, 9), (10, 3), (7, -1)] with energy 0.0
Accept Update!
Step=6, Beta=2.9859839999999997, [(10, 3), (6, 8), (1, 5), (4, 7), (9, -1)] with energy 0.0
Accept Update!
Step=7, Beta=3.5831807999999996, [(4, 7), (10, 6), (3, 8), (1, 9), (5, -1)] with energy 0.0
Step=8, Beta=4.299816959999999, [(4, 7), (10, 6), (3, 8), (1, 9), (5, -1)] with energy 0.0
Step=9, Beta=5.159780351999999, [(4, 7), (10, 6), (3, 8), (1, 9), (5, -1)] with energy 0.0

```

| round_1 | round_2 | round_3 | round_4 |
| ------- | ------- | ------- | ------- |
| 2       | 3       | 4       | 9       |
| 1       | 4       | 6       | 0       |
| 4       | 1       | 5       | 8       |
| 3       | 2       | 1       | 7       |
| 6       | 6       | 3       | -1      |
| 5       | 5       | 2       | 10      |
| 0       | 0       | 0       | 3       |
| 0       | 0       | 0       | 1       |
| 0       | 0       | 0       | 6       |
| 0       | 0       | 0       | 4       |
