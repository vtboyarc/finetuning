# a script to download models from huggingface hub for trying to convert to gguf
from huggingface_hub import snapshot_download
model_id="mlx-community/mistral-7B-v0.1"
snapshot_download(repo_id=model_id, local_dir="mistral",
                  local_dir_use_symlinks=False, revision="main")