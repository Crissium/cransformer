import torch
import torch.nn as nn
from model import Cracker
from data import gen_data_in_batch
from config import LEN_TEXT


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
size_batch = 600
num_epoches = 100000
checkpointing = 2500
num_test_batches = 1000
model = Cracker().to(device)
criterion = nn.CrossEntropyLoss()
optimiser = torch.optim.Adam(model.parameters())

def train() -> None:
	total_loss = 0.
	for i in range(num_epoches):
		plain, cipher = gen_data_in_batch(size_batch)
		plain = plain.to(device)
		cipher = cipher.to(device)
		optimiser.zero_grad()
		# Note we are trying to break the cipher (not to encrypt)
		output = model(cipher, plain)
		# Shape of output: (LEN_TEXT, size_batch, embedding_dim)
		# Shape of target (plain): (LEN_TEXT, size_batch)
		# The expected shape of input to the cross entropy loss: (size_batch * LEN_TEXT, embedding_dim)
		loss = criterion(output.reshape(-1, output.shape[-1]), plain.reshape(-1))
		total_loss += loss.item()
		loss.backward()
		optimiser.step()
		if i % checkpointing == 0:
			print(f'Epoch {i}, loss: {total_loss / checkpointing}')
			total_loss = 0.
			torch.save(model.state_dict(), f'model_{i // checkpointing:04d}.pth')

			predicted = torch.argmax(output, dim=-1)
			print(''.join([chr(c + ord('A')) for c in plain[:, 0]]))
			print(''.join([chr(c + ord('A')) for c in predicted[:, 0]]))

def evaluate() -> None:
	model.eval()
	total_loss = 0.
	num_correct = 0
	for i in range(num_test_batches):
		plain, cipher = gen_data_in_batch(size_batch)
		plain = plain.to(device)
		cipher = cipher.to(device)
		output = model(cipher, plain)
		loss = criterion(output.reshape(-1, output.shape[-1]), plain.reshape(-1))
		total_loss += loss.item()
		num_correct += torch.sum(torch.argmax(output, dim=-1) == plain).item()
	accuracy = num_correct / (num_test_batches * size_batch * LEN_TEXT)
	print(f'Accuracy: {accuracy}')
	print(f'Loss: {total_loss / num_test_batches}')

if __name__ == '__main__':
	train()
	evaluate()