# Fine tuning LLMs using Apple MLX

##  Steps

### generating jsonl files to be used for fine tuning
For generating the train and valid jsonl files, need to have ollama running with a model that is specified in the generate script such as mistral. Don't need to have it running in cli, just have ollama itself running with the given model pulled. This model doesn't need to be the same as the one you fine tune on, this step is just for generating the answers to the prompts, to create the jsonl files

note: change the file name in generate.php/.py Whichever file you use. need to change the file name of your prompt json file in 2 places (I've called mine instructions.json).

You need to have a json file of the prompts you want answers to generated. You can ask an LLM to do this for you!
Once you have the file completed with your prompts, run the generate script to generate the answers, it will output two files: train.jsonl and valid.jsonl - these will be the two files you need for fine tuning
I store these 2 files in a data folder.

php generate.php


### fine tuning
Clone this repo: https://github.com/ml-explore/mlx-examples

git pull in Desktop/mlx-examples repo to get changes
pip install -U mlx

For exmapled, I cloned it to my Desktop.
cd into: Desktop/mlx-examples/lora
for running the fine tuning on a mlx model.

For getting a model to fine tune, from huggingface just manually download config.json, tokenizer.model, and weights.npz, add to the mlx-model folder

or can download with the download.py script. If the model doesn't at least have the above 3 files, it won't work to fine tune
Note: make sure to change the --model path to the folder of whatever model it is you want to fine tune

The data folder is location of the 2 jsonl files
python lora.py \
 --train \
 --model /Users/adamcarter/Desktop/finetuning/mistral \
 --data /Users/adamcarter/Desktop/finetuning/data \
 --batch-size 2 \
 --lora-layers 8 \
 --iters 1000



### Note: MLX also supports any model directly from huggingface! No need to download a model first
in the --model line just put the path to the model on HF
change path of data if different folders with different jsonl files for different fine tunes
 smaller parameter models train much faster, can do more lora-layers and iterations also
 python lora.py \
  --train \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --data /Users/adamcarter/Desktop/finetuning/data \
  --batch-size 2 \
  --lora-layers 8 \
  --iters 1000


  ### less memory intensive if have issues (can also do less iters):
   python lora.py \
  --train \
  --model mistralai/Mistral-7B-Instruct-v0.2 \
  --data /Users/adamcarter/Desktop/finetuning/data_marcus \
  --batch-size 1 \
  --lora-layers 4 \
  --iters 1000


  ### to try with gguf files once supported with MLX:
   python lora.py \
  --train \
  --model TheBloke/Mistral-7B-Instruct-v0.2-GGUF \
  --data /Users/adamcarter/Desktop/finetuning/data_marcus \
  --batch-size 1 \
  --lora-layers 4 \
  --iters 1000

## After fine tuning
note: make sure you use the same model that you ran the fine tuning against
in: mlx-examples/lora

copy the adapters.npz from the mlx-examples/lora directory. This is the results of your fine tuning you ran above!

 python lora.py \
 --model /Users/adamcarter/Desktop/finetuning/mistral \
 --adapter-file /Users/adamcarter/Desktop/finetuning/adapters.npz \
 --max-tokens 512 \
 --prompt "How did Marcus Aurelius apply Stoicism to his role as a Roman Emperor?"

Another  way to run prompts against fine tune, using model path directly from HF instead of having the model locally

don't forget after fine tuning, to copy adapters.npz from mlx-examples/lora to in here or wherever the path is using for that

 python lora.py \
 --model mistralai/Mistral-7B-Instruct-v0.2  \
 --adapter-file /Users/adamcarter/Desktop/finetuning/adapters.npz \
 --max-tokens 512 \
 --prompt "How did Marcus Aurelius apply Stoicism to his role as a Roman Emperor?"