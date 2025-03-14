import torch
import torch.nn as nn
import torch.nn.functional as F

from config import args


class Actor(nn.Module):
	def __init__(self, state_dim, action_dim, max_action):
		super(Actor, self).__init__()

		self.l1 = nn.Linear(state_dim, 256)
		self.l2 = nn.Linear(256, 256)
		self.l3 = nn.Linear(256, action_dim)
		
		self.max_action = torch.from_numpy(max_action).to(torch.float32).detach().to(args.device)
		

	def forward(self, state):

		a = F.relu(self.l1(state))
		a = F.relu(self.l2(a))

		return self.max_action * torch.tanh(self.l3(a))


class Critic(nn.Module):
	def __init__(self, state_dim, action_dim):
		super(Critic, self).__init__()

		# Q1 architecture
		self.l1 = nn.Linear(state_dim + action_dim, 256)
		self.l2 = nn.Linear(256, 256)
		self.l3 = nn.Linear(256, 1)

		# Q2 architecture
		self.l4 = nn.Linear(state_dim + action_dim, 256)
		self.l5 = nn.Linear(256, 256)
		self.l6 = nn.Linear(256, 1)


	def forward(self, state, action):
		
		s_a = torch.cat([state, action], dim=-1)

		q1 = F.relu(self.l1(s_a))
		q1 = F.relu(self.l2(q1))
		q1 = self.l3(q1)

		q2 = F.relu(self.l4(s_a))
		q2 = F.relu(self.l5(q2))
		q2 = self.l6(q2)

		return q1, q2


	def forward_Q1(self, state, action):
		
		s_a = torch.cat([state, action], dim=-1)

		q1 = F.relu(self.l1(s_a))
		q1 = F.relu(self.l2(q1))
		q1 = self.l3(q1)

		return q1




