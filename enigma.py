import random
import string
from rotor import *
from config import LEN_TEXT, NUM_PLUGS

class Enigma:
	"""Represents an Enigma machine.
	Initializes an Enigma machine with these arguments:
	- ref: reflector;
	- r1, r2, r3: rotors;
	- key: initial state of rotors;
	- plus: plugboard settings.
	"""

	def __init__(self, ref, r1, r2, r3, plugs, key="AAA", ring="AAA"):
		"""Initialization of the Enigma machine."""
		self.reflector = ref
		self.rotor1 = r1
		self.rotor2 = r2
		self.rotor3 = r3

		self.rotor1.state = key[0]
		self.rotor2.state = key[1]
		self.rotor3.state = key[2]
		self.rotor1.ring = ring[0]
		self.rotor2.ring = ring[1]
		self.rotor3.ring = ring[2]
		self.reflector.state = "A"

		alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		alpha_out = [" "] * 26
		for i in range(len(alpha)):
			alpha_out[i] = alpha[i]
		for k, v in plugs:
			alpha_out[ord(k) - ord("A")] = v
			alpha_out[ord(v) - ord("A")] = k

		try:
			self.transtab = str.maketrans(alpha, "".join(alpha_out))
		except:
			# Python 2
			from string import maketrans

			self.transtab = maketrans(alpha, "".join(alpha_out))

	def encipher(self, plaintext_in):
		"""Encrypt 'plaintext_in'."""
		ciphertext = ""
		plaintext_in_upper = plaintext_in.upper()
		plaintext = plaintext_in_upper.translate(self.transtab)
		for c in plaintext:

			# ignore non alphabetic char
			if not c.isalpha():
				ciphertext += c
				continue

			if self.rotor1.is_in_turnover_pos() and self.rotor2.is_in_turnover_pos():
				self.rotor3.notch()
			if self.rotor1.is_in_turnover_pos():
				self.rotor2.notch()

			self.rotor1.notch()

			t = self.rotor1.encipher_right(c)
			t = self.rotor2.encipher_right(t)
			t = self.rotor3.encipher_right(t)
			t = self.reflector.encipher(t)
			t = self.rotor3.encipher_left(t)
			t = self.rotor2.encipher_left(t)
			t = self.rotor1.encipher_left(t)
			ciphertext += t

		res = ciphertext.translate(self.transtab)

		fres = ""
		for idx, char in enumerate(res):
			if plaintext_in[idx].islower():
				fres += char.lower()
			else:
				fres += char
		return fres

	def __str__(self):
		"""Pretty display."""
		return """
		Reflector: {}

		Rotor 1: {}

		Rotor 2: {}

		Rotor 3: {}""".format(
			self.reflector, self.rotor1, self.rotor2, self.rotor3
		)


FIXED_PREFIX = 'ANX' # German for 'to'
FIXED_CONTENT = 'KEINEXBESONDERENXEREIGNISSE' # German for 'no special events'
FIXED_PLUGBOARD = [('A', 'B'), ('C', 'D'), ('E', 'F'), ('G', 'H'), ('I', 'J'), ('K', 'L'), ('M', 'N'), ('O', 'P'), ('Q', 'R'), ('S', 'T')]

def gen_plain_cipher_weak() -> tuple[str, str]:
	# plugs : list[tuple[str, str]] = []
	# to_be_swapped = random.sample(string.ascii_uppercase, 2 * NUM_PLUGS)
	# for i in range(NUM_PLUGS):
	# 	plugs.append((to_be_swapped[2 * i], to_be_swapped[2 * i + 1]))
	engine = Enigma(ROTOR_Reflector_B, ROTOR_I, ROTOR_II, ROTOR_III, FIXED_PLUGBOARD) # Wehrmacht Enigma (M3)
	random_content = ''.join([random.choice(string.ascii_uppercase) for _ in range(LEN_TEXT - len(FIXED_PREFIX) - len(FIXED_CONTENT))])
	random_division_point = random.randint(0, len(random_content) - 1)
	plain = FIXED_PREFIX + random_content[:random_division_point] + FIXED_CONTENT + random_content[random_division_point:]
	cipher = engine.encipher(plain)
	return plain, cipher

def gen_plain_cipher_weak_no_pattern() -> tuple[str, str]:
	engine = Enigma(ROTOR_Reflector_B, ROTOR_I, ROTOR_II, ROTOR_III, FIXED_PLUGBOARD)
	plain = ''.join([random.choice(string.ascii_uppercase) for _ in range(LEN_TEXT)])
	cipher = engine.encipher(plain)
	return plain, cipher

def gen_plain_cipher_fixed_rotors_random_plugboard() -> tuple[str, str]:
	plugs = []
	to_be_swapped = random.sample(string.ascii_uppercase, 2 * NUM_PLUGS)
	for i in range(NUM_PLUGS):
		plugs.append((to_be_swapped[2 * i], to_be_swapped[2 * i + 1]))
	engine = Enigma(ROTOR_Reflector_B, ROTOR_I, ROTOR_II, ROTOR_III, plugs)
	plain = ''.join([random.choice(string.ascii_uppercase) for _ in range(LEN_TEXT)])
	cipher = engine.encipher(plain)
	return plain, cipher

rotors = (ROTOR_I, ROTOR_II, ROTOR_III, ROTOR_IV, ROTOR_V)
def gen_plain_cipher_random_rotors_random_plugboard() -> tuple[str, str]:
	plugs = []
	to_be_swapped = random.sample(string.ascii_uppercase, 2 * NUM_PLUGS)
	for i in range(NUM_PLUGS):
		plugs.append((to_be_swapped[2 * i], to_be_swapped[2 * i + 1]))
	engine = Enigma(ROTOR_Reflector_B, *random.sample(rotors, 3), plugs)
	plain = ''.join([random.choice(string.ascii_uppercase) for _ in range(LEN_TEXT)])
	cipher = engine.encipher(plain)
	return plain, cipher

def gen_plain_cipher_random_rotors_random_rotor_positions_random_ring_random_plugboard() -> tuple[str, str]:
	plugs = []
	to_be_swapped = random.sample(string.ascii_uppercase, 2 * NUM_PLUGS)
	for i in range(NUM_PLUGS):
		plugs.append((to_be_swapped[2 * i], to_be_swapped[2 * i + 1]))
	engine = Enigma(ROTOR_Reflector_B, *random.sample(rotors, 3), plugs, key=''.join([random.choice(string.ascii_uppercase) for _ in range(3)]), ring=''.join([random.choice(string.ascii_uppercase) for _ in range(3)]))
	plain = ''.join([random.choice(string.ascii_uppercase) for _ in range(LEN_TEXT)])
	cipher = engine.encipher(plain)
	return plain, cipher