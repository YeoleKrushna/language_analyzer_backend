from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch, os
import requests
import zipfile



MODEL_PATH = "lang_analyzer_200k_model"
MODEL_URL = "https://github.com/YeoleKrushna/language_analyzer_backend/releases/download/v1/lang_analyzer_200k_model.zip"  

# -----------------------------
# Download & unzip model if missing
# -----------------------------
if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    r = requests.get(MODEL_URL, stream=True)
    with open("model.zip", "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            f.write(chunk)
    print("Unzipping model...")
    with zipfile.ZipFile("model.zip", "r") as zip_ref:
        zip_ref.extractall(MODEL_PATH)
    os.remove("model.zip")
    print("Model ready!")


# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def correct_sentence(text: str) -> str:
    """
    Corrects a single sentence or batch of sentences.
    Input:
        text: str or list of str
    Returns:
        corrected sentence (str) or list of corrected sentences
    """
    # Convert single string to list for batch processing
    single_input = False
    if isinstance(text, str):
        text = [text]
        single_input = True

    # Tokenize and move to device
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )
    inputs.pop("token_type_ids", None)  # Some models don't use token_type_ids
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Generate corrected sentences
    outputs = model.generate(
        **inputs,
        max_length=128,
        num_beams=5,
        early_stopping=True
    )

    # Decode outputs
    corrected = [tokenizer.decode(out, skip_special_tokens=True) for out in outputs]

    return corrected[0] if single_input else corrected
