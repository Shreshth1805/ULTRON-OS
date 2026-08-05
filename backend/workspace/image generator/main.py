```python
import argparse
import json
import os
import torch
from src.data_loader import DataLoader
from src.model import Generator, Discriminator
from src.trainer import Trainer
from src.utils import calculate_metrics

def main():
    parser = argparse.ArgumentParser(description='HyperRealix')
    parser.add_argument('--config', type=str, default='experiments/config.json', help='path to config file')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    # Set up device (GPU or CPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load data
    data_loader = DataLoader(config['data_path'], config['batch_size'])
    train_loader, val_loader, test_loader = data_loader.get_loaders()

    # Initialize models
    generator = Generator(config['generator_params']).to(device)
    discriminator = Discriminator(config['discriminator_params']).to(device)

    # Initialize trainer
    trainer = Trainer(generator, discriminator, config['trainer_params'], device)

    # Train model
    trainer.train(train_loader, val_loader)

    # Evaluate model
    metrics = calculate_metrics(generator, test_loader, device)
    print('Model metrics:', metrics)

    # Save model
    torch.save(generator.state_dict(), 'results/generator.pth')
    torch.save(discriminator.state_dict(), 'results/discriminator.pth')

if __name__ == '__main__':
    main()
```