#!/usr/bin/env python3
"""
YOLO12 Model Training Script
Train YOLO12 model for rune detection
"""

import argparse
import yaml
from pathlib import Path
from ultralytics import YOLO
import torch


class RuneTrainer:
    """Train YOLO12 model for rune detection"""

    def __init__(self, config_path='config.yaml'):
        """
        Initialize trainer with configuration

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self.load_config()
        print("Trainer initialized")
        print(f"Configuration loaded from: {config_path}")

    def load_config(self):
        """Load configuration from YAML file"""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def train(self, data_yaml=None, model_name=None, epochs=None, batch_size=None, img_size=None):
        """
        Train YOLO12 model

        Args:
            data_yaml: Path to dataset YAML file (overrides config)
            model_name: Model architecture name (overrides config)
            epochs: Number of training epochs (overrides config)
            batch_size: Batch size (overrides config)
            img_size: Image size (overrides config)
        """
        # Get training parameters from config or arguments
        data_yaml = data_yaml or self.config['dataset']['data_yaml']
        model_name = model_name or self.config['model']['architecture']
        epochs = epochs or self.config['training']['epochs']
        batch_size = batch_size or self.config['training']['batch_size']
        img_size = img_size or self.config['training']['img_size']

        print("\n" + "="*60)
        print("Training Configuration")
        print("="*60)
        print(f"Model: {model_name}")
        print(f"Dataset: {data_yaml}")
        print(f"Epochs: {epochs}")
        print(f"Batch size: {batch_size}")
        print(f"Image size: {img_size}")
        print(f"Device: {self.config['training']['device']}")
        print("="*60 + "\n")

        # Check if data.yaml exists
        if not Path(data_yaml).exists():
            print(f"Error: Dataset YAML file not found: {data_yaml}")
            print("\nPlease ensure you have:")
            print("1. Downloaded a dataset using roboflow_integration.py")
            print("2. Updated the data_yaml path in config.yaml")
            return None

        # Initialize model
        print(f"Initializing {model_name} model...")

        # Check if pretrained weights are specified
        pretrained = self.config['model'].get('pretrained')
        if pretrained and Path(pretrained).exists():
            print(f"Loading pretrained weights from: {pretrained}")
            model = YOLO(pretrained)
        else:
            print(f"Using default pretrained weights for {model_name}")
            model = YOLO(f'{model_name}.pt')

        # Training arguments
        train_args = {
            'data': data_yaml,
            'epochs': epochs,
            'batch': batch_size,
            'imgsz': img_size,
            'device': self.config['training']['device'],
            'workers': self.config['training']['workers'],
            'optimizer': self.config['training']['optimizer'],
            'lr0': self.config['training']['learning_rate'],
            'amp': self.config['training']['amp'],
            'save_period': self.config['training']['save_period'],
            'patience': self.config['training']['patience'],
            'project': self.config['output']['model_dir'],
            'name': 'rune_detection',
            'exist_ok': True,
            'verbose': True
        }

        print("\nStarting training...")
        print("This may take a while depending on your hardware and dataset size.\n")

        try:
            # Train model
            results = model.train(**train_args)

            print("\n" + "="*60)
            print("Training completed successfully!")
            print("="*60)
            print(f"\nModel saved to: {self.config['output']['model_dir']}/rune_detection")
            print(f"Best weights: {self.config['output']['model_dir']}/rune_detection/weights/best.pt")
            print(f"Last weights: {self.config['output']['model_dir']}/rune_detection/weights/last.pt")
            print("\nTo use the trained model for detection:")
            print(f"  python detect_rune.py --source <image/video> --model {self.config['output']['model_dir']}/rune_detection/weights/best.pt")

            return results

        except Exception as e:
            print(f"\nError during training: {e}")
            print("\nTroubleshooting:")
            print("1. Check if CUDA is available if using GPU")
            print("2. Reduce batch size if out of memory")
            print("3. Verify dataset YAML file is correct")
            print("4. Ensure dataset images are accessible")
            return None

    def validate(self, model_path=None, data_yaml=None):
        """
        Validate trained model

        Args:
            model_path: Path to trained model
            data_yaml: Path to dataset YAML file
        """
        model_path = model_path or self.config['model']['custom_model']
        data_yaml = data_yaml or self.config['dataset']['data_yaml']

        if not Path(model_path).exists():
            print(f"Error: Model not found: {model_path}")
            return None

        print(f"\nValidating model: {model_path}")
        print(f"Dataset: {data_yaml}")

        model = YOLO(model_path)

        try:
            results = model.val(data=data_yaml, device=self.config['training']['device'])

            print("\n" + "="*60)
            print("Validation Results")
            print("="*60)
            print(f"mAP50: {results.box.map50:.4f}")
            print(f"mAP50-95: {results.box.map:.4f}")
            print("="*60)

            return results

        except Exception as e:
            print(f"Error during validation: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description='Train YOLO12 model for rune detection')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    parser.add_argument('--data', type=str, help='Path to dataset YAML file')
    parser.add_argument('--model', type=str, help='Model architecture (yolo12n, yolo12s, etc.)')
    parser.add_argument('--epochs', type=int, help='Number of epochs')
    parser.add_argument('--batch', type=int, help='Batch size')
    parser.add_argument('--img-size', type=int, help='Image size')
    parser.add_argument('--validate', action='store_true', help='Run validation only')
    parser.add_argument('--model-path', type=str, help='Path to model for validation')

    args = parser.parse_args()

    # Initialize trainer
    trainer = RuneTrainer(config_path=args.config)

    if args.validate:
        # Run validation
        trainer.validate(model_path=args.model_path, data_yaml=args.data)
    else:
        # Run training
        trainer.train(
            data_yaml=args.data,
            model_name=args.model,
            epochs=args.epochs,
            batch_size=args.batch,
            img_size=args.img_size
        )


if __name__ == '__main__':
    main()
