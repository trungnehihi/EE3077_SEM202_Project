import torch
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import lab2rgb

def lab_to_rgb(L, ab):
  L = (L + 1.) * 50.
  ab = ab * 110.

  Lab = torch.cat([L, ab], dim=1).permute(0, 2, 3, 1).cpu().numpy()

  rgb_imgs = []
  for img in Lab:
    img_rgb = lab2rgb(img)
    rgb_imgs.append(img_rgb)

  return np.stack(rgb_imgs, axis=0)

def visualize(model, data, lead, save=True):
  model.G.eval()

  with torch.no_grad():
    model.setup_input(data)
    model.forward()

  model.G.train()

  fake_color = model.fake_color.detach()
  real_color = model.ab
  L = model.L

  fake_imgs = lab_to_rgb(L, fake_color)
  real_imgs = lab_to_rgb(L, real_color)

  fig = plt.figure(figsize=(15, 8))
  for i in range(5):
    ax = plt.subplot(3, 5, i + 1)
    ax.imshow(L[i][0].cpu(), cmap="gray")
    ax.axis("off")
    ax = plt.subplot(3, 5, i + 1 + 5)
    ax.imshow(fake_imgs[i])
    ax.axis("off")
    ax = plt.subplot(3, 5, i + 1 + 10)
    ax.imshow(real_imgs[i])
    ax.axis("off")
  plt.show()

  if save:
    fig.savefig(f"./images/colorization_{lead}_{time.time()}.png")