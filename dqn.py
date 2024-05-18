import gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

class DQNNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 128)
        self.output_layer = nn.Linear(128, action_size)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.output_layer(x)


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = DQNNetwork(state_size, action_size)
        self.optimizer = optim.Adam(
            self.model.parameters(), lr=self.learning_rate)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, use_epsilon=True):
        if use_epsilon and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        act_values = self.model(state)
        return np.argmax(act_values.detach().numpy())

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state).unsqueeze(0)
                target = (reward + self.gamma *
                          np.amax(self.model(next_state).detach().numpy()))
            state = torch.FloatTensor(state).unsqueeze(0)
            target_f = self.model(state)
            target_f[0][0][action] = target
            self.optimizer.zero_grad()
            loss = nn.MSELoss()(self.model(state), target_f)
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, env, episodes, batch_size=32):
        for e in range(episodes):
            state = env.reset()[0]
            state = np.reshape(state, [1, self.state_size])
            for time in range(200):
                action = self.act(state)
                next_state, reward, done, _, _ = env.step(action)
                reward = reward if not done else -10
                next_state = np.reshape(next_state, [1, self.state_size])
                self.remember(state, action, reward, next_state, done)
                state = next_state
                if done:
                    print("episode: {}/{}, score: {}, e: {:.2}".format(e,
                          episodes, time, self.epsilon))
                    break
                if len(self.memory) > batch_size:
                    self.replay(batch_size)
            print("episode: {}/{}, score: {}, e: {:.2}".format(e,
                                                               episodes, time, self.epsilon))

    def save_model(self, name, episodes):
        file_name = 'models/' + name + '-' + str(episodes) + '.pth'
        torch.save(self.model.state_dict(), file_name)

    def load_model(self, name, episodes):
        file_name = 'models/' + name + '-' + str(episodes) + '.pth'
        self.model.load_state_dict(torch.load(file_name))
        self.model.eval()  # Set the model to evaluation mode

    def test(self, env):
        self.epsilon = 0  # Disable epsilon-greedy action selection
        state = env.reset()[0]
        state = np.reshape(state, [1, self.state_size])
        done = False
        while not done:
            env.render()
            action = self.act(state, use_epsilon=False)
            state, _, done, _, _ = env.step(action)
            state = np.reshape(state, [1, self.state_size])


if __name__ == "__main__":
    mode = 'test'  # 'train' or 'test'
   # mode = 'train'  # 'train' or 'test'
    name = 'CartPole-v1'
    episodes = 100
    if mode == 'train':
        env = gym.make(name)
    else:
        env = gym.make(name, render_mode="human")

    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)

    if mode == 'train':
        agent.train(env, episodes)
        agent.save_model(name, episodes)
    elif mode == 'test':
        agent.load_model(name, episodes)
        agent.test(env)
