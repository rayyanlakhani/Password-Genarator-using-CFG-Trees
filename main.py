import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to load stopwords from a file
def load_stopwords(file_path):
    with open(file_path, "r") as file:
        return set(line.strip().lower() for line in file)

# Function to remove stopwords from a phrase
def remove_stopwords(phrase, stopwords):
    return [word for word in phrase.split() if word.lower() not in stopwords]

# ParseTree class to represent the transformation tree
class ParseTree:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

    def traverse(self):
        if not self.children:
            return self.value
        return ''.join(child.traverse() for child in self.children)

# Function to create a complex parse tree based on the word
def create_complex_parse_tree(word):
    if not word:
        return None

    if len(word) == 1:
        return ParseTree(value=random.choice([word.upper(), word.lower()]))

    rule = random.choice(["W D S", "W S", "D W", "W"])
    if rule == "W D S":
        return ParseTree(
            value="S",
            children=[
                create_complex_parse_tree(word[:-1]),
                ParseTree(value=random.choice("0123456789!@#$%^&*")),
                ParseTree(value=word[-1])
            ]
        )
    elif rule == "W S":
        return ParseTree(
            value="S",
            children=[
                create_complex_parse_tree(word[:-1]),
                ParseTree(value=word[-1].upper())
            ]
        )
    elif rule == "D W":
        return ParseTree(
            value="S",
            children=[
                ParseTree(value=random.choice("0123456789!@#$%^&*")),
                create_complex_parse_tree(word)
            ]
        )
    else:  # W
        return ParseTree(
            value="W",
            children=[ParseTree(value=char) for char in word]
        )

# Function to generate a password based on a phrase
def generate_password(phrase, stopwords):
    words = remove_stopwords(phrase, stopwords)
    password = ""
    for word in words:
        tree = create_complex_parse_tree(word)
        password += tree.traverse()
    return password

# API route to generate password via POST request
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    phrase = data.get("phrase", "")
    if not phrase:
        return jsonify({"error": "No phrase provided"}), 400

    password = generate_password(phrase, stopwords)
    return jsonify({"password": password})

if __name__ == '__main__':
    # Load stopwords from a file before starting Flask app
    stopwords = load_stopwords("stopwords.txt")
    app.run(debug=True)
