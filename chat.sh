echo "Run Ollama movie export model via python"
echo "Example questions..."
echo
echo "Give me the top 3 grossing films in 2020"
echo "Give me the top 3 comedy films"
echo "Give me the top 10 files with a score over 5/10"
echo "Give me the top grossing movies in json format"
echo

python3 -m venv .venv
source .venv/bin/activate
python3 chat.py