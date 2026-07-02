import json
import random
from datasets import load_dataset
import os

def prepare_data():
    print("Loading box office dataset from Hugging Face...")
    # Load the specific dataset
    dataset = load_dataset("jason1966/aditya126_movies-box-office-dataset-2000-2024", split="train")

    # Split into train (95%) and validation (5%)
    dataset_split = dataset.train_test_split(test_size=0.05, seed=42)
    train_data = dataset_split["train"]
    valid_data = dataset_split["test"]

    # System prompt to give the model a persistent identity
    system_prompt = "You are a movie box office analytics expert. Provide accurate financial data regarding films released between 2000 and 2024."

    def row_to_jsonl(row):
        """
        Dynamically translates a tabular row of movie statistics into conversational prompts.
        Adjust the column names if your specific version uses lowercase or variations.
        """
        # Extract features (handling potential missing/null values gracefully)
        title = row.get("Release Group") or row.get("title") or "Unknown Movie"
        year = row.get("Year") or row.get("year") or "Unknown Year"
        genres = row.get("Genres") or row.get("genres") or "Unknown"
        worldwide = row.get("$Worldwide") or row.get("worldwide_gross") or "N/A"
        rating = row.get("Rating") or row.get("rating") or "N/A"

        # Varied question templates so the model learns flexibility
        templates = [
            {
                "user": f"What are the box office stats for the movie '{title}'?",
                "assistant": f"The movie '{title}' was released in {year}. It falls under the genres of {genres}, holds an average audience score/rating of {rating}, and pulled in a total worldwide gross of ${worldwide}."
            },
            {
                "user": f"How much money did '{title}' ({year}) make worldwide?",
                "assistant": f"'{title}' ({year}) grossed approximately ${worldwide} globally."
            },
            {
                "user": f"Can you tell me the genre and rating of the movie '{title}'?",
                "assistant": f"'{title}' is classified under {genres} and has an experimental or aggregate score of {rating}."
            }
        ]

        # Randomly choose one variations style per movie row to ensure diverse training data
        selected = random.choice(templates)

        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": selected["user"]},
                {"role": "assistant", "content": selected["assistant"]}
            ]
        }

    os.makedirs("./movie_data", exist_ok=True)

    # Process and write files
    for split, data in [("movie_data/train", train_data), ("movie_data/valid", valid_data)]:
        filename = f"{split}.jsonl"
        with open(filename, "w", encoding="utf-8") as f:
            for row in data:
                # Skip broken or completely empty entries
                # if not row.get("Title") and not row.get("title"):
                #     continue
                formatted = row_to_jsonl(row)
                f.write(json.dumps(formatted) + "\n")
        print(f"Successfully generated {filename} with {len(data)} entries.")

if __name__ == "__main__":
    prepare_data()