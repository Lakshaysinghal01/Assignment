import requests
import json
import pandas as pd


def fetch_data(api_url, output_file):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def analyze_data(input_file):
    try:
        with open(input_file, "r") as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        total_posts = len(df)
        unique_users = df["userId"].nunique()
        avg_words_per_post = df["body"].apply(lambda x: len(x.split())).mean()
        return total_posts, unique_users, avg_words_per_post
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error analyzing data: {e}")
        return 0, 0, 0


def generate_summary(output_file, total_posts, unique_users, avg_words_per_post):
    try:
        with open(output_file, "w") as file:
            file.write(f"Total Posts: {total_posts}\n")
            file.write(f"Unique Users: {unique_users}\n")
            file.write(f"Average Words per Post: {avg_words_per_post:.2f}\n")
    except IOError as e:
        print(f"Error writing summary: {e}")


if __name__ == "__main__":
    API_URL = "https://jsonplaceholder.typicode.com/posts"
    DATA_FILE = "data.json"
    SUMMARY_FILE = "summary.txt"

    # Fetch data from the API
    data = fetch_data(API_URL, DATA_FILE)

    # Analyze the data
    total_posts, unique_users, avg_words = analyze_data(DATA_FILE)

    # Generate summary file
    generate_summary(SUMMARY_FILE, total_posts, unique_users, avg_words)

    print("Task completed. Check summary.txt for results.")
