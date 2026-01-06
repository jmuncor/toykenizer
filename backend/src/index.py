import json
import traceback
from urllib.parse import urlparse
from workers import Response # type: ignore
from tokenizers.bpe import BPETokenizer

# A helper function to make sending JSON responses easier.
def json_response(data, status=200):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    return Response(json.dumps(data), status=status, headers=headers)

async def on_fetch(request, env):
    try:
        # Handle CORS preflight requests
        if request.method == "OPTIONS":
            return Response(None, status=204, headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            })

        # Determine which endpoint is being called from the URL path.
        parsed_url = urlparse(request.url)
        path = parsed_url.path

        if request.method != "POST":
            return json_response({"error": f"Method {request.method} not allowed. Please use POST."}, status=405)

        # --- Endpoint: /api/train ---
        if path == "/api/train":
            body_text = await request.text()
            body = json.loads(body_text)
            text_to_train = body.get("text")
            vocab_size = body.get("vocab_size", 512)

            if not text_to_train:
                return json_response({"error": "Request body must include 'text' key."}, status=400)

            tokenizer = BPETokenizer()
            tokenizer.train(text_to_train, vocab_size)

            return json_response(tokenizer.save())

        # --- Endpoint: /api/encode ---
        elif path == "/api/encode":
            body_text = await request.text()
            body = json.loads(body_text)
            model_data = body.get("model")
            text_to_encode = body.get("text")

            if not model_data or not text_to_encode:
                return json_response({"error": "Request body must include 'model' and 'text' keys."}, status=400)
            
            tokenizer = BPETokenizer()
            tokenizer.load(model_data)
            
            tokens = tokenizer.encode(text_to_encode)
            return json_response({"tokens": tokens})

        # --- Endpoint: /api/decode ---
        elif path == "/api/decode":
            body_text = await request.text()
            body = json.loads(body_text)
            model_data = body.get("model")
            tokens_to_decode = body.get("tokens")

            if not model_data or tokens_to_decode is None:
                return json_response({"error": "Request body must include 'model' and 'tokens' keys."}, status=400)

            tokenizer = BPETokenizer()
            tokenizer.load(model_data)
            
            text = tokenizer.decode(tokens_to_decode)
            return json_response({"text": text})

        else:
            return json_response({"error": "Not Found. Available endpoints: /api/train, /api/encode, /api/decode"}, status=404)

    except Exception:
        trace = traceback.format_exc()
        print(f"Error: {trace}")
        return json_response({"error": "An internal server error occurred"}, status=500)