# Documentation - Traffic Neural Network

## Loading Data

Before I wanted to jump into implementing different neural networks, I had to nail the data processing. I had a dataset of 43 different street signs each type in a different folder. I iterated through the whole dataset and when I entered a new folder the label's name was set to be equal to the folder's name. However, I wasn't done yet. I needed to gather the pictures aswell. This loop was perfect for that, so I just had to get the PATH of every image with the help of cv2. Also, I had to resize it so that every picture would be equal in size.

## First Neural Network

For the first try I wanted to implement something basic with a very few hidden layers. This was a good idea because I could test out if my data loading was on point, and I had a good comparison for the more advanced neural networks I create later on.

- Configuration:
  - Convolution: **filters: 3, kernel_size: 3x3, activation: relu**
  - Pooling: **None**
  - Hidden Layer: **neurons: 32, activation: sigmoid**
- Results: **accuracy: 0.8369 - 676ms/epoch**

I was expecting a lower accuracy form my first neural network, since my only goal was to make it pretty simple. With this in mind, I had to come up with big adjustments to make my following neural networks even better.

## Second Neural Network

For the second try my goal was to think about all the activation funcions and to bring in more convolution and pooling layers. I did not want to add more hidden layers just yet, my goal was to make it as proficient as I can with the least layers.

- Configuration:
  - Convolution: **filters: 32, kernel_size: 3x3, activation: sigmoid**
  - Pooling: **size: 3x3**
  - Hidden Layer: **neurons: 128, activation: relu**
  - Optimizer: **Gradient Descend**
- Results: **accuracy: 0.9560 - 934ms/epoch**

My second try got a 12% improvement, and I was very happy with that. Now it is time to scale up the neural network. My goal was to scale it, but to avoid overfitting at all cost.

## Third Neural Network

After a lot of testing I have managed to squeeze out a 4% improvement from the last network. Throughout the testing I realized that more hidden layers did not result in a better result, so I turned towards the convolutional and pooling layers. I added 1-1 to both and it resulted in a big improvement. I also tested out the network with relu activation functions, but the Sigmoid generated a better result.

- Configuration:
  - Convolution: **filters: 64, 64, kernel_size: 3x3, 3x3, activation: sigmoid, sigmoid**
  - Pooling: **size: 2x2, 2x2**
  - Hidden Layer: **neurons: 64, activation: sigmoid**
  - Optimizer: **adam**
- Results: **accuracy: 0.9924 - 2s/epoch**

All in all, the computation time increased by a second which is not a good result, but getting a 99.24% is a very nice precentage.
