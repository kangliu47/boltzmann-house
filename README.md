# BoltzmannHouse

![BoltzmannHouse Logo](/assets/logo_boltzmannhouse.webp)

Welcome to **BoltzmannHouse**, an avant-garde coffee shop where science, individuality, and exceptional brews converge. The story begins with Ludwig Boltzmann, the brilliant physicist known for his pioneering work in statistical mechanics and thermodynamics. Upon discovering that his contemporary, James Clerk Maxwell, had his name associated with a commercial coffee brand—Maxwell House—Boltzmann felt a spark of inspiration (and perhaps a touch of competitive spirit).

Determined not to let the essence of scientific inquiry be diluted by commercial interests, Boltzmann envisioned a coffee house that would embody the true principles of physics. BoltzmannHouse was born—a place where every detail, from the roasting of beans to the pairing of patrons, adheres strictly to the laws of statistical physics.

At BoltzmannHouse, no two visits are the same. The coffee experience is meticulously personalized, reflecting Boltzmann's commitment to individuality and entropy. By applying his famous entropy formula to the art of coffee making, each cup is crafted to match the unique preferences and "energy states" of the customer. The result is a dynamic menu that evolves with the patrons' tastes, ensuring that your coffee is as unique as you are.

But Boltzmann didn't stop at coffee. He extended his scientific approach to fostering connections among guests. Recognizing that meaningful interactions enhance the overall experience, BoltzmannHouse employs an innovative pairing system inspired by statistical mechanics. By considering the "interaction energy" based on past conversations and applying a time-decaying function, guests are paired in ways that maximize novelty and minimize redundancy. It's social networking taken to a whole new, scientifically grounded level.

In subtle homage (and perhaps a gentle tease) to Maxwell's commercial venture, BoltzmannHouse stands as a testament to the purity of scientific principles applied to everyday life. It's not just a coffee shop; it's an experiment in social dynamics, a celebration of individuality, and a haven for those who appreciate the nuanced interplay between science and daily experiences.

Step into BoltzmannHouse, where every cup and every conversation is a fresh discovery governed by the elegant laws of physics.

---

## About This Project

BoltzmannHouse is an open-source Python project that brings this imaginative scenario to life through code. Inspired by Ludwig Boltzmann's contributions to statistical physics, the project aims to optimize social pairings and personalize experiences by:

Minimizing Repeat Interactions: Utilizing a time-decaying "interaction energy" to reduce the likelihood of recent pairings reoccurring, promoting fresh and engaging conversations.
Enhancing Personalization: Adapting pairing algorithms to individual preferences, much like customizing coffee to match a patron's unique taste profile.

Adhering to Scientific Principles: Applying the Boltzmann distribution and concepts like inverse temperature to simulate and control randomness in social pairings.
Visualizing Social Networks: Providing interactive dashboards and network visualizations to represent pairing histories and current configurations, allowing users to observe and understand the dynamics at play.

Resisting Commercial Dilution: Staying true to the foundational principles of statistical physics without compromising for commercial simplicity, much like Boltzmann's commitment to scientific integrity over mass-market appeal.

By fusing the rigor of scientific methodology with the warmth of social interaction, BoltzmannHouse offers a novel approach to enhancing connectivity in groups, organizations, or any setting where fostering meaningful interactions is valuable.

_Join us in exploring how the profound principles of physics can enrich our social fabric, one personalized experience at a time._

---

## Technical Setup

---

## Data Structure

### Pairing History

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
