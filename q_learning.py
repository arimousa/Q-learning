import itertools
import sys
import numpy as np
from collections import defaultdict, namedtuple

EpisodeStats = namedtuple("Stats", ["episode_lengths", "episode_rewards"])


def make_epsilon_greedy_policy(Q, epsilon, nA):
    """
    Creates an epsilon-greedy policy based on a given Q-function and epsilon.

    Args:
      Q: A dictionary that maps from state -> action-values.
        Each value is a numpy array of length nA (see below)
      epsilon: The probability to select a random action . float between 0 and 1.
      nA: Number of actions in the environment.

    Returns:
      A function that takes the observation as an argument and returns
      the probabilities for each action in the form of a numpy array of length nA.
    """

    def policy_fn(observation):
        policy = np.ones(nA)
        policy *= epsilon / nA
        best_action = np.argmax(Q[observation])
        policy[best_action] += 1 - epsilon
        return policy

    return policy_fn


def q_learning(env, num_episodes, discount_factor=1.0, alpha=0.5, epsilon=0.1):
    """
    Q-Learning algorithm: Off-policy TD control. Finds the optimal greedy policy
    while following an epsilon-greedy policy

    Args:
      env: environment.
      num_episodes: Number of episodes to run for.
      discount_factor: Lambda time discount factor.
      alpha: TD learning rate.
      epsilon: Chance the sample a random action. Float betwen 0 and 1.

    Returns:
      A tuple (Q, episode_lengths).
      Q is the optimal action-value function, a dictionary mapping state -> action values.
      stats is an EpisodeStats object with two numpy arrays for episode_lengths and episode_rewards.
    """

    # The final action-value function.
    # A nested dictionary that maps state -> (action -> action-value).
    Q = defaultdict(lambda: np.zeros(env.nA))
    # Keeps track of useful statistics

    stats = EpisodeStats(
        episode_lengths=np.zeros(num_episodes),
        episode_rewards=np.zeros(num_episodes))

    # The policy we're following
    policy = make_epsilon_greedy_policy(Q, epsilon, env.nA)
    for i_episode in range(num_episodes):
        # Print out which episode we're on, useful for debugging.
        if (i_episode + 1) % 100 == 0:
            print("\rEpisode {}/{}.".format(i_episode + 1, num_episodes), end="")
            sys.stdout.flush()
        state = env.reset()
        for i in itertools.count():

            action_probs = policy(state)
            print('action_probs: ', action_probs)
            action = np.random.choice(4, p=action_probs)
            print('action: ', action)
            next_state, reward, done, prob = env.step(action)
            best_next_action = np.argmax(Q[next_state])

            stats.episode_rewards[i_episode] += reward
            stats.episode_lengths[i_episode] = i

            Q[state][action] += alpha * (
                        reward + discount_factor * np.max(Q[next_state][best_next_action]) - Q[state][action])
            print('Q[state]: ', Q[state])

            if done:
                break
            state = next_state
    return Q, stats
