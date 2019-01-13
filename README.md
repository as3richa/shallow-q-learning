# shallow-q-learning

Pedagogical implementation of Q-learning applied to a toy problem, using only [Christopher J. C. H. Watkins' 1992 technical note](https://dl.acm.org/citation.cfm?id=139618) as a reference.

As formulated in Watkins, Q-learning is an optimization algorithm that allows an agent to learn a tabular representation of an optimal policy for a controlled Markov process. In plain English, the algorithm computes an explicit mapping from _every possible state/action pair_ to the expected returns of taking that action in that state. From this mapping it's trivial to reconstruct an explicit policy. Under mild conditions and given an infinite number of episodes from which to learn, Q-learning is shown in Watkins to converge to an optimal policy.

Contrast deep Q-learning, in which the expected returns are estimated using a deep neural network rather than an exhaustive tabular mapping. Deep Q-learning can be applied to problems with much larger state and action spaces, because it doesn't need to allocate space for every single state/action pair; moreover, it needn't be trained against every possible state/action pair (the expectation being that the neural network will learn useful generalizations between similar states).

## The Task

The agent is piloting a spaceship through a discrete 2-dimensional grid. The grid is littered with obstacles, and contains exactly one goal; cells containing neither an obstacle nor the goal are empty.

The ship always points in a cardinal direction; in any given state, the agent can either fly one cell forwards, or rotate 90 degrees clockwise or counterclockwise. If ever the agent leaves the bounds of the grid or flys into a cell containing an obstacle, the ship crashes. It's guaranteed that there exists a path to the goal for every empty cell.

The task is to learn a policy such that, for any initial empty cell and direction, following the policy will eventually lead the agent to the goal without crashing.

## Is this useful or interesting?

No. The task has no nondeterminism, so applying Q-learning to it basically boils down to memorizing an optimal solution in a slow and agonizing derivation process. My only goal in solving this problem was to familiarize myself with the literature a bit more.
