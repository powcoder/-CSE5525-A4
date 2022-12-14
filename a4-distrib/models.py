https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
# models.py

import numpy as np
import random
import time
import collections

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from torch.autograd import Variable as Var


class LanguageModel(object):

    def get_next_char_log_probs(self, context) -> np.ndarray:
        """
        Returns a log probability distribution over the next characters given a context.
        The log should be base e
        :param context: a single character to score
        :return: A numpy vector log P(y | context) where y ranges over the output vocabulary.
        """
        raise Exception("Only implemented in subclasses")


    def get_log_prob_sequence(self, next_chars, context) -> float:
        """
        Scores a bunch of characters following context. That is, returns
        log P(nc1, nc2, nc3, ... | context) = log P(nc1 | context) + log P(nc2 | context, nc1), ...
        The log should be base e
        :param next_chars:
        :param context:
        :return: The float probability
        """
        raise Exception("Only implemented in subclasses")


class UniformLanguageModel(LanguageModel):
    def __init__(self, voc_size):
        self.voc_size = voc_size

    def get_next_char_log_probs(self, context):
        return np.ones([self.voc_size]) * np.log(1.0/self.voc_size)

    def get_log_prob_sequence(self, next_chars, context):
        return np.log(1.0/self.voc_size) * len(next_chars)


class RNNLanguageModel(LanguageModel):
    def __init__(self, model_emb, model_dec, vocab_index):
        self.model_emb = model_emb
        self.model_dec = model_dec
        self.vocab_index = vocab_index

    def get_next_char_log_probs(self, context):

        # Hint: check the train_rnn_lm to see how to cal the RNN model correctly 
        
        raise Exception("Implement me")

    def get_log_prob_sequence(self, next_chars, context):
        raise Exception("Implement me")


class TransformerLanguageModel(LanguageModel):
    def __init__(self, model_dec, vocab_index):
        self.model_dec = model_dec
        self.vocab_index = vocab_index

    def get_next_char_log_probs(self, context):
        raise Exception("Implement me")

    def get_log_prob_sequence(self, next_chars, context):
        raise Exception("Implement me")




# Embedding layer that has a lookup table of symbols that is [full_dict_size x input_dim]. Includes dropout.
# Works for both non-batched and batched inputs
class EmbeddingLayer(nn.Module):
    # Parameters: dimension of the word embeddings, number of words, and the dropout rate to apply
    # (0.2 is often a reasonable value)
    def __init__(self, input_dim, full_dict_size, embedding_dropout_rate):
        super(EmbeddingLayer, self).__init__()
        self.dropout = nn.Dropout(embedding_dropout_rate)
        self.word_embedding = nn.Embedding(full_dict_size, input_dim)

    # Takes either a non-batched input [sent len x input_dim] or a batched input
    # [batch size x sent len x input dim]
    def forward(self, input):
        embedded_words = self.word_embedding(input)
        final_embeddings = self.dropout(embedded_words)
        return final_embeddings



#####################
#     RNN Decoder   #
#####################



class RNNDecoder(nn.Module):
    def __init__(self, input_size, hidden_size, output_dict_size, dropout, rnn_type='lstm'):
        super(RNNDecoder, self).__init__()
        self.n_layers = 1
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.cell_input_size = input_size
        self.rnn_type = rnn_type
        if rnn_type == 'gru':
            self.rnn = nn.GRU(self.cell_input_size, hidden_size, dropout=dropout)
        elif rnn_type == 'lstm':
            self.rnn = nn.LSTM(self.cell_input_size, hidden_size, num_layers=1, dropout=dropout)
        else:
            raise NotImplementedError
        # output should be batch x output_dict_size
        self.output_layer = nn.Linear(hidden_size, output_dict_size)
        # print(f"Out dict size {output_dict_size}")
        self.log_softmax_layer = nn.LogSoftmax(dim=1)
        self.init_weight()

    def init_weight(self):
        if self.rnn_type == 'lstm':
            nn.init.xavier_uniform_(self.rnn.weight_hh_l0, gain=1)
            nn.init.xavier_uniform_(self.rnn.weight_ih_l0, gain=1)

            nn.init.constant_(self.rnn.bias_hh_l0, 0)
            nn.init.constant_(self.rnn.bias_ih_l0, 0)
        elif self.rnn_type == 'gru':
            nn.init.xavier_uniform_(self.rnn.weight.data, gain=1)

    def forward(self, embedded_input, state):
        
        # Hint: you've implemented simlar things in your HW#3

        raise Exception("Implement me")




#####################
#Transformer Decoder#
#####################



class TransformerDecoder(nn.Module):
  # classification task
  def __init__(self, d, h, depth, max_len, vocab_size, num_classes):
    super(TransformerDecoder, self).__init__()
    self.token_emb = nn.Embedding(vocab_size, d)
    self.pos_emb = nn.Embedding(max_len, d)

    trans_blocks = []
    for i in range(depth):
      trans_blocks.append(TransformerBlock(d, h, mask=True))
    self.trans_blocks = nn.Sequential(*trans_blocks)

    self.out_layer = nn.Linear(d, num_classes)

  def forward(self, x):

    # step 1: get token and position embeddings

    # step 2: pass them through Transformer blocks

    # step 3: pass the outputlayer 

    # step 4: pass the log_softmax layer 

    raise Exception("Implement me")


class TransformerBlock(nn.Module):
    def __init__(self, d, h, mask):
        super(TransformerBlock, self).__init__()

        self.attention = SelfAttention(d, h, mask=mask)

        self.norm_1 = nn.LayerNorm(d)
        self.norm_2 = nn.LayerNorm(d)

        self.ff = nn.Sequential(
            nn.Linear(d, 4 * d),
            nn.ReLU(),
            nn.Linear(4 * d, d)
        )

    def forward(self, x):

        # step 1: self-attention

        # step 2: residual + layer norm

        # step 3: FFN/MLP

        # step 4: residual + layer norm

        raise Exception("Implement me")


class SelfAttention(nn.Module):
    def __init__(self, d, h=8, mask=False):
        super(SelfAttention, self).__init__()
        # d: dimension
        # heads: number of heads
        self.d, self.h = d, h
        self.mask = mask
        self.linear_key = nn.Linear(d, d * h, bias=False)
        self.linear_query = nn.Linear(d, d * h, bias=False)
        self.linear_value = nn.Linear(d, d * h, bias=False)
        self.linear_unify = nn.Linear(d * h, d)

    def forward(self, x):

        # step 1: transform x to key/query/value 

        # step 2: scaled do product between key and query to get attention

        # step 3: casual masking (you may use torch.triu_indices)

        # step 4: softmax over attention

        # step 5: multiply attention with value 

        # step 6: another linear layer for output

        raise Exception("Implement me")



