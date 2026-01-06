# Toykenizer Backend (Cloudflare Worker)

This directory contains the Cloudflare Worker implementation for the tokenization backend.

## Structure

*   `src/`: Contains the Python source code for the Cloudflare Worker.
    *   `tokenizers/bpe.py`: The Byte Pair Encoding (BPE) implementation.
    *   `index.py`: The main Cloudflare Worker handler, which loads the BPE model and handles API requests.
*   `scripts/`: Contains utility scripts (e.g., `train_bpe.py` which was used once to generate the model). This directory is empty after setup.
*   `wrangler.toml`: Configuration file for Cloudflare Workers.

The trained BPE model and its training data are located in the top-level `models/harry-potter-tokenizer/` directory:
*   `models/harry-potter-tokenizer/text.txt`: The text used to train the BPE model (e.g., Harry Potter books). **This file is NOT deployed with the Worker.**
*   `models/harry-potter-tokenizer/bpe_model.json`: The trained BPE model, which IS deployed with the Worker as an asset.

## Setup & Deployment

Follow these steps to deploy your Cloudflare Worker:

### 1. Install Wrangler

If you don't have it already, install Cloudflare's Wrangler CLI tool globally:

```bash
npm install -g wrangler
```

### 2. Authenticate Wrangler

Authenticate Wrangler with your Cloudflare account. This will open a browser window for you to log in.

```bash
wrangler login
```

### 3. Deploy the Worker

Navigate to the `backend/` directory and deploy your Worker.

```bash
cd backend
wrangler deploy
```

Wrangler will build and deploy your Worker. It will output the URL where your Worker is accessible.

### 4. Testing the API

Once deployed, you can test your API endpoints. The Worker exposes two endpoints: `/api/encode` and `/api/decode`.

**Encode Example (POST request):**

```bash
curl -X POST <YOUR_WORKER_URL>/api/encode \
-H "Content-Type: application/json" \
-d '{"text": "Hello, world!"}'
```

**Decode Example (POST request):**

```bash
curl -X POST <YOUR_WORKER_URL>/api/decode \
-H "Content-Type: application/json" \
-d '{"tokens": [108, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]}'
```
(Note: The tokens in the decode example are illustrative and depend on your trained model.)

## Local Development (Optional)

You can also run the Worker locally for testing purposes:

```bash
cd backend
wrangler dev --local
```

This will start a local development server, usually on `http://127.0.0.1:8787`. You can then use `curl` commands against this local URL.
