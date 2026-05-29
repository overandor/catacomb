#!/usr/bin/env python3
"""Train ML model for virality and usefulness prediction."""
import os
import argparse
from ml_prediction_agent import ViralityUsefulnessDataset, ModelTrainer


def collect_training_data(github_token: str, repos_file: str, output_file: str, limit: int = 1000):
    """Collect training data from repositories."""
    print(f"Collecting training data from {repos_file}...")
    
    # Read repo list
    with open(repos_file, 'r') as f:
        repos = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(repos)} repositories to process")
    
    # Collect data
    dataset = ViralityUsefulnessDataset(github_token)
    training_data = dataset.collect_training_data(repos, limit)
    
    print(f"Collected {len(training_data)} training examples")
    
    # Save data
    import json
    with open(output_file, 'w') as f:
        json.dump(training_data, f, indent=2)
    
    print(f"Saved training data to {output_file}")
    
    return training_data


def train_model(data_file: str, model_output: str):
    """Train ML model on collected data."""
    print(f"Training model on {data_file}...")
    
    # Load data
    import json
    with open(data_file, 'r') as f:
        training_data = json.load(f)
    
    print(f"Loaded {len(training_data)} training examples")
    
    # Train model
    trainer = ModelTrainer()
    metrics = trainer.train(training_data)
    
    print("Training complete!")
    print("Metrics:")
    print(f"  Virality - MSE: {metrics['virality']['mse']:.4f}, R2: {metrics['virality']['r2']:.4f}")
    print(f"  Usefulness - MSE: {metrics['usefulness']['mse']:.4f}, R2: {metrics['usefulness']['r2']:.4f}")
    
    # Save model
    trainer.save_model(model_output)
    print(f"Saved model to {model_output}")
    
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Train Catacomb ML model")
    parser.add_argument('--github-token', help='GitHub API token')
    parser.add_argument('--repos-file', required=True, help='File containing list of repos (owner/repo per line)')
    parser.add_argument('--data-output', default='training_data.json', help='Output file for training data')
    parser.add_argument('--model-output', default='catacomb_model.joblib', help='Output file for trained model')
    parser.add_argument('--limit', type=int, default=1000, help='Maximum repos to collect')
    parser.add_argument('--skip-collection', action='store_true', help='Skip data collection if data file exists')
    
    args = parser.parse_args()
    
    # Collect data
    if not args.skip_collection or not os.path.exists(args.data_output):
        collect_training_data(
            args.github_token,
            args.repos_file,
            args.data_output,
            args.limit
        )
    
    # Train model
    train_model(args.data_output, args.model_output)


if __name__ == "__main__":
    main()
