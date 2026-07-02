export OLLAMA_KEEP_ALIVE=0m

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

echo Install dependencies ...
pip install -r requirements.txt

echo install Ollama ...
curl -fsSL https://ollama.com/install.sh | sh

echo
echo "** Building model based on jason1966/aditya126_movies-box-office-dataset-2000-2024 dataset"
echo

echo Preparing Dataset ...
python prepare_data.py

echo Fine Tuning ...
mlx_lm.lora \
--model mlx-community/Ministral-3-3B-Instruct-2512 \
--train \
--data ./movie_data \
--iters 200 \
--adapter-path ./adapters
--resume-adapter-file ./adapters/adapters.safetensors

#echo Fine Tuning (append training data to model) ...
#mlx_lm.lora \
#--model mlx-community/Ministral-3-3B-Instruct-2512 \
#--train \
#--data ./movie_data \
#--iters 200 \
#--adapter-path ./adapters \
#--resume-adapter-file ./adapters/adapters.safetensors

echo Fusing Model ...
mlx_lm.fuse \
--model mlx-community/Ministral-3-3B-Instruct-2512 \
--adapter-path ./adapters \
--save-path ./fused_model

echo Create Ollama Model
ollama create movie-expert -f ./Modelfile
