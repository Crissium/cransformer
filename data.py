import torch
import random
import string
from enigma import gen_plain_cipher_random_rotors_random_rotor_positions_random_ring_random_plugboard
from config import LEN_TEXT

def tabula_recta_encrypt(plain: str, key: str) -> str:
	"""
	`plain` and `key` are both single characters.
	"""
	return chr((ord(plain) - ord('A') + ord(key) - ord('A')) % 26 + ord('A'))

PRIMER = 'DATASCIENCE'
def gen_plain_cipher_autokey() -> tuple[str, str]:
	plain = ''.join((random.choice(string.ascii_uppercase) for _ in range(LEN_TEXT)))
	key = PRIMER + plain[:-len(PRIMER)]
	cipher = ''.join((tabula_recta_encrypt(plain[i], key[i]) for i in range(LEN_TEXT)))
	return plain, cipher

SHIFT = 3
def gen_plain_cipher_caesar() -> tuple[str, str]:
	plain = ''.join((random.choice(string.ascii_uppercase) for _ in range(LEN_TEXT)))
	cipher = ''.join((chr((ord(c) - ord('A') + SHIFT) % 26 + ord('A')) for c in plain))
	return plain, cipher

gen_plain_cipher = gen_plain_cipher_random_rotors_random_rotor_positions_random_ring_random_plugboard
def gen_data_in_batch(size_batch: int) -> tuple[torch.Tensor, torch.Tensor]:
	batch_plain, batch_cipher = zip(*[gen_plain_cipher() for _ in range(size_batch)])
	cipher_numerical = torch.tensor([[ord(c) - ord('A') for c in cipher] for cipher in batch_cipher])
	plain_numerical = torch.tensor([[ord(c) - ord('A') for c in plain] for plain in batch_plain])
	return plain_numerical.permute(1, 0), cipher_numerical.permute(1, 0)