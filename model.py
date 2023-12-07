import torch
import torch.nn as nn
from config import LEN_TEXT

class PositionalEncoding(nn.Module):
	def __init__(self, d_model: int) -> None:
		super(PositionalEncoding, self).__init__()
		self.dropout = nn.Dropout(p=0.1)

		pe = torch.zeros(LEN_TEXT, d_model)
		position = torch.arange(0, LEN_TEXT, dtype=torch.float).unsqueeze(1)
		div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-torch.log(torch.tensor(10000.0)) / d_model))
		pe[:, 0::2] = torch.sin(position * div_term)
		pe[:, 1::2] = torch.cos(position * div_term)
		pe = pe.unsqueeze(0).transpose(0, 1)
		self.register_buffer('pe', pe)

	def forward(self, x: torch.Tensor) -> torch.Tensor:
		x = x + self.pe[:x.size(0), :]
		return self.dropout(x)

class Cracker(nn.Module):
	def __init__(self) -> None:
		super().__init__()
		self.transformer = nn.Transformer(d_model=32, activation='gelu')
		self.embedding = nn.Embedding(26, self.transformer.d_model)
		self.pos_encoder = PositionalEncoding(self.transformer.d_model)

	def forward(self, cipher: torch.Tensor, plain: torch.Tensor) -> torch.Tensor:
		source = self.embedding(cipher)
		source = self.pos_encoder(source)
		target = self.embedding(plain)
		target = self.pos_encoder(target)
		return self.transformer(source, target)
