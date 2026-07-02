# FineTuneHelloWorld

A minimal **hello-world** example of fine-tuning an AI model locally on **Apple Silicon** using **MLX** and serving it with **Ollama**.

This repository demonstrates a full, practical loop:

1. Prepare a small conversational training dataset.
2. Fine-tune a base model with LoRA on Apple Silicon.
3. Fuse adapters into final weights.
4. Package and run the model in Ollama.

## What each key file does

### `prepare_data.py`
Builds the training and validation data used for fine-tuning.

- Loads a movie box-office dataset from Hugging Face.
- Converts rows into randomized question/answer conversations.
- Writes output in JSONL chat format for MLX training.
- Produces:
  - `train_data.jsonl`
  - `valid_data.jsonl`

In short: this script turns tabular movie data into instruction-style examples the model can learn from.

### `build.sh`
Automates the end-to-end workflow.

- Creates and activates a Python virtual environment.
- Installs dependencies (including `mlx-lm` and Ollama Python tooling).
- Runs `prepare_data.py` to generate training data.
- Starts LoRA fine-tuning with `mlx_lm.lora`. 
- Fuses the adapter into a final model with `mlx_lm.fuse`.
- Registers the final model with Ollama using the local `Modelfile`.

In short: this is the "one command" pipeline from raw data to a usable Ollama model.

'build.sh' also includes a `--resume` option to continue training from a previous checkpoint if needed.

### `Modelfile`
Defines how Ollama should load and run the fine-tuned model.

- Points Ollama to the fused model weights.
- Sets base runtime parameters (for example temperature).
- Provides system-level behavior/instructions for the assistant persona.

In short: this file is the Ollama packaging/config layer for the model produced by training.

### `chat.sh`
Shows how to interface with the model from Python using a small wrapper script.

- Prints example prompts to get started quickly.
- Activates the repository Python virtual environment if needed.
- Runs `chat.py`, which uses the `ollama` Python library for streaming chat responses.

In short: this is an example of programmatic model interaction from Python rather than only using the Ollama CLI.

**Usage:**

```zsh
./chat.sh
```

## Typical workflow

Build the training data, fine-tune the model, and register it with Ollama:
```zsh
./build.sh
```

Demo to chat with the model using the Ollama command line interface:

```zsh
./demo.sh
```

## Why this repo exists

This project is intentionally small and focused. It is meant to be a clear, reproducible starting point for learning how local fine-tuning works on Apple Silicon with Ollama, before scaling up to larger datasets, longer runs, or more advanced model configurations.
