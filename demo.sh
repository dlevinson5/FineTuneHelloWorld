echo "Run Ollama model chat (Ask questions about movies from 2000-2024)"
echo "Example questions..."
echo
echo "Give me the top 3 grossing films in 2020"
echo "Give me the top 3 comedy films"
echo "Give me the top 10 files with a score over 5/10"
echo

ollama run movie-assistant

echo Stopping model ...
ollama stop movie-expert:latest