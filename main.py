import random

class ParseTree:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

    def traverse(self):
        # Traverse the tree to generate the transformed word
        if not self.children:
            return self.value
        return ''.join(child.traverse() for child in self.children)

def create_complex_parse_tree(word):
    
    if not word:
        return None

    if len(word) == 1:
        return ParseTree(
            value=random.choice([word.upper(), word.lower()])
        )


    rule = random.choice(["W D S", "W S", "D W", "W"])  # Choose a complex rule
    if rule == "W D S":
        return ParseTree(
            value="S",
            children=[
                create_complex_parse_tree(word[:-1]),  # Recursive on word
                ParseTree(value=random.choice("0123456789!@#$%^&*")),  # Add digit/symbol
                ParseTree(value=word[-1])  # Use the last character as-is
            ]
        )
    elif rule == "W S":
        return ParseTree(
            value="S",
            children=[
                create_complex_parse_tree(word[:-1]),  # Recursive on word
                ParseTree(value=word[-1].upper())  # Capitalize the last character
            ]
        )
    elif rule == "D W":
        return ParseTree(
            value="S",
            children=[
                ParseTree(value=random.choice("0123456789!@#$%^&*")),  # Add digit/symbol
                create_complex_parse_tree(word)  # Recursive on word
            ]
        )
    else:  # W
        return ParseTree(
            value="W",
            children=[ParseTree(value=char) for char in word]
        )

def remove_stopwords(phrase, stopwords):
    return [word for word in phrase.split() if word.lower() not in stopwords]

def generate_password(phrase, stopwords):
    """
    Generate a password by applying complex CFG transformations.
    """
    words = remove_stopwords(phrase, stopwords)
    password = ""
    for word in words:
        tree = create_complex_parse_tree(word)  # Build parse tree
        password += tree.traverse()  # Generate password from tree
    return password

if __name__ == "__main__":
    # Load stopwords from a file
    def load_stopwords(file_path):
        with open(file_path, "r") as file:
            return set(line.strip().lower() for line in file)

    stopwords = load_stopwords("stopwords.txt")
    user_phrase = input("Enter a phrase: ")

    # Generate the password
    password = generate_password(user_phrase, stopwords)
    print("Generated Password:", password)
