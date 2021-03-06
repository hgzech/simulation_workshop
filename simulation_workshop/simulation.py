# AUTOGENERATED! DO NOT EDIT! File to edit: 02_wilson_figure.ipynb (unless otherwise specified).

__all__ = ['choose', 'simulate_M3RescorlaWagner_v1', 'plot_rescorla_game', 'simulate_M4ChoiceKernel_v1',
           'plot_choice_kernel_game']

# Cell
import numpy as np

# Cell
def choose(p):
    chosen_action = None
    rand = np.random.random() # Choses float from continuous uniform distribution between 0 and 1
    if rand < p[0]: # If our random number is smaller than our first p
        chosen_action = 0 # ...return index of first action
    else:
        chosen_action = 1
    return chosen_action

# Cell
def simulate_M3RescorlaWagner_v1(T, mu, alpha, beta, starting_q_values = [.5, .5]):
    Q = np.array(starting_q_values) # Q are the Q-values the participant currently holds for each action
    Qs = []
    deltas = []
    actions = [] # the participants actions
    rewards = [] # the rewards received by the participant
    # Looping through trials
    for t in range(T):
        Qs.append(Q.copy())
        p = np.exp(Q*beta) / sum(np.exp(Q*beta)) # The probability with which a participant choses each action
        action = choose(p) # The choice of the participant based on the choice probabilities
        actions.append(action)
        reward = np.random.random() < mu[action] # The reward determined by the game for the action the participant chose
        rewards.append(int(reward))
        delta = reward - Q[action] # prediction error
        deltas.append(delta)
        Q = list(Q)
        Q[action] = Q[action] + alpha * delta
        Q = np.array(Q)

    return actions, rewards, Qs, deltas


# Cell
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def plot_rescorla_game(T, mu, alpha, beta):
    fig, ax = plt.subplots(1,1, figsize = (16,8))
    actions, rewards, Qs, deltas = simulate_M3RescorlaWagner_v1(T, mu, alpha, beta)
    df = pd.DataFrame(Qs)
    df['pe'] = pd.Series(deltas, name = 'delta')
    df.columns = ['Q1','Q2','pe']
    df.pe.plot(alpha = .5)
    df.Q1.plot()
    df.Q2.plot()
    sns.despine()
    plt.legend()
    ax.set_ylim([-1,1])

# Cell
def simulate_M4ChoiceKernel_v1(T, mu, alpha_c, beta_c):
    choice_kernel = np.array([0, 0]) # choice_kernel are the choice_kernel-values the participant currently holds for each action
    choice_kernels = []
    actions = [] # the participants actions
    rewards = [] # the rewards received by the participant
    # Looping through trials
    for t in range(T):
        choice_kernels.append(choice_kernel)
        p = np.exp(beta_c*choice_kernel)/sum(np.exp(beta_c*choice_kernel)) # The probability with which a participant choses each action
        action = choose(p) # The choice of the participant based on the choice probabilities
        actions.append(action)
        reward = np.random.random() < mu[action] # The reward determined by the game for the action the participant chose
        rewards.append(int(reward))
        choice_kernel = (1 - alpha_c) * choice_kernel # This is a general choice kernel decay
        choice_kernel[action] = choice_kernel[action] + alpha_c * 1 # Stickiness
    return actions, rewards, choice_kernels


# Cell
def plot_choice_kernel_game(T, mu, alpha, beta):
    fig, ax = plt.subplots(1,1, figsize = (16,8))
    actions, rewards, Cks = simulate_M4ChoiceKernel_v1(T, mu, alpha, beta)
    df = pd.DataFrame(Cks)
    df.columns = ['Ck1','Ck2']
    df.Ck1.plot()
    df.Ck2.plot()
    sns.despine()
    plt.legend()
    ax.set_ylim([-.2,1.1])

    # Adding actions
    action_df = pd.DataFrame({'action':actions})
    action_df['trial'] = action_df.index
    action_df['y'] = -.1
    action_df['action'] = action_df.action.replace({0:'1',1:'2'})
    sns.scatterplot(x = 'trial', y = 'y', hue = 'action', data = action_df, ax = ax, hue_order = ['1','2'])

    return actions