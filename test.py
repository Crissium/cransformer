import torch
import torch.nn as nn
import sys
from config import LEN_TEXT
from model import Cracker
from data import gen_data_in_batch

if __name__ == '__main__':
	model_name = sys.argv[1]
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	model = Cracker().to(device)
	model.load_state_dict(torch.load(model_name, map_location=device))
	model.eval()
	size_batch = 10
	num_test_batches = 10
	total_loss = 0.
	num_correct = 0
	criterion = nn.CrossEntropyLoss()
	for i in range(num_test_batches):
		plain, cipher = gen_data_in_batch(size_batch)
		plain = plain.to(device)
		cipher = cipher.to(device)
		output = model(cipher, plain)
		loss = criterion(output.reshape(-1, output.shape[-1]), plain.reshape(-1))
		total_loss += loss.item()
		num_correct += torch.sum(torch.argmax(output, dim=-1) == plain).item()
		
		# Let's see what sort of output we get
		predicted = torch.argmax(output, dim=-1)
		for j in range(size_batch):
			print(''.join([chr(c + ord('A')) for c in cipher[:, j]]))
			print(''.join([chr(c + ord('A')) for c in predicted[:, j]]))
			print(''.join([chr(c + ord('A')) for c in plain[:, j]]))
			print()
	accuracy = num_correct / (num_test_batches * size_batch * LEN_TEXT)
	print(f'Accuracy: {accuracy}')
	print(f'Loss: {total_loss / num_test_batches}')

	