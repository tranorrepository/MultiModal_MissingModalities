from datageneration.datagenerator import MatrixProjection
from datageneration.datagenerator import RandomMatrixProjection
from datageneration.datagenerator import SubsetsLatentZ3

from models.autoencoder import Autoencoder
from models.autoencoder import MultiAutoencoder
from utils.time import timeSince
from utils.launcher import launcher_predict

import torch.nn as nn
import torch.optim as optim

import numpy as np
import time
import torch
import math

#### Data Generation
#%% Define projector

N = 3
dim_z = 3
dim_input = 2
subset3 = SubsetsLatentZ3(noise_variance=1e-2)
z = np.random.normal(size=(dim_z, 1))
samples = subset3.sample(z, noise=True)

"""
N = 3
projection = MatrixProjection(dim_z, dim_input, N, noise_variance=1e-2)
randomprojection = RandomMatrixProjection(dim_z, dim_input, N, noise_variance=1e-2)
"""



#### PyTorch
#%% PyTorch


net = Autoencoder(dim_input, 10, 3, 10, dim_input)
lr = 0.0001
criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=lr)
n_iter = int(1e3)
n_epoch = 20
idx_in, idx_target = 0, 0

#launcher_predict(net, subset3, criterion, optimizer, n_epoch, n_iter, (idx_in, idx_target), plot=True)

 #%% Pytorch auto encoder multiple modalities



encoder_layer_1_size = 3
encoder_layer_2_size = 3
decoder_layer_1_size = 3
decoder_layer_2_size = 3

multiencoder = MultiAutoencoder(dim_input,
                                encoder_layer_1_size, encoder_layer_2_size,
                            decoder_layer_1_size, decoder_layer_2_size,
                            N)



multiencoder.zero_grad()
loss = 0


#z_in = np.random.normal(size=(dim_z, 1))
#multi_x = subset3.sample(z_in, noise=True)

#z_latent = multiencoder.fusion(multiencoder.encoder(multi_x))
#out = multiencoder.forward(multi_x)



#loss = criterion(torch.cat(out).view(N, 1, dim_input), torch.cat(samples))  # Not sure here with the dimensions
#loss.backward(retain_graph=True)


#%%      #   launch

# Create the NN
encoder_layer_1_size = 10
encoder_layer_2_size = 3
decoder_layer_1_size = 3
decoder_layer_2_size = 3

multiencoder = MultiAutoencoder(dim_input, encoder_layer_1_size, encoder_layer_2_size,
                            decoder_layer_1_size, decoder_layer_2_size,
                            N)

## Launch parameters
lr = 0.0001
criterion = nn.MSELoss()
optimizer = optim.Adam(multiencoder.parameters(), lr=lr)

batch_size = int(1e1)
n_iter = int(1e3)
n_epoch = 10

start = time.time()


for epoch in range(n_epoch):
    for i in range(n_iter):

        z_in = np.random.normal(size=(dim_z, 1))
        multi_x = subset3.sample(z_in, noise=True)

        # Randomly remove modalities

        # Initialize hidden, grad, loss
        multiencoder.zero_grad()
        loss = 0

        output = multiencoder.latent(multi_x)
        #loss = criterion(torch.cat(output).view(N, 1, dim_input), torch.cat(multi_x)) # Not sure here with the dimensions
        loss = criterion(output, torch.FloatTensor(z_in).view(1, -1)) # Not sure here with the dimensions

        # Gradient step
        loss.backward(retain_graph=True)
        optimizer.step()

    print("Epoch {0}, {1} : {2}".format(epoch, timeSince(start), loss.data.view(-1).numpy()[0]))


#%% Learned Representation

z_in = np.random.normal(size=(dim_z, 1))
multi_x = subset3.sample(z_in, noise=True)
z_latent = multiencoder.fusion(multiencoder.encoder(multi_x))