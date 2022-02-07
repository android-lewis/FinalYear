import torch
import torch.optim as optim
import api.gan.config as config
import uuid
from torchvision.utils import save_image
from math import log2
from api.gan.model import (
    Generator
)
from pathlib import Path

checkpoint = Path("api/gan/checkpoints/generator.pth")
Path(f"api/images/generated/").mkdir(parents=True, exist_ok=True)
gen = Generator(config.Z_DIM, config.IN_CHANNELS, img_channels=config.CHANNELS_IMG).to(config.DEVICE)
opt_gen = optim.Adam(gen.parameters(), lr=config.LEARNING_RATE, betas=(0.0, 0.99))
lr = config.LEARNING_RATE
n = 1

def generate_image(checkpoint_file, model, optimizer, lr, n):
    print("=> Loading checkpoint")
    checkpoint = torch.load(checkpoint_file, map_location="cpu")
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])

    # If we don't do this then it will just have learning rate of old checkpoint
    # and it will lead to many hours of debugging \:
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr
    
    gen.eval()
    alpha = 1.0
    name = ""
    with torch.no_grad():
        noise = torch.randn(1, config.Z_DIM, 1, 1).to(config.DEVICE)
        steps = int(log2(config.START_TRAIN_AT_IMG_SIZE / 4))
        img = gen(noise, alpha, steps)
        name = str(uuid.uuid4())
        print("=> Saving image")
        save_image(img*0.5+0.5, f"api/images/generated/{name}.png")
    
    
    print("=> Images Generated")
    return f"{name}.png"

def generate():
    return generate_image(checkpoint, gen, opt_gen, lr, n)

