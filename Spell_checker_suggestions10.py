import tkinter as tk


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

    def suggest(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._dfs(node, prefix)

    def _dfs(self, node, prefix):
        results = []
        if node.is_word:
            results.append(prefix)
        for char in node.children:
            results.extend(self._dfs(node.children[char], prefix + char))
        return results

    def autocomplete(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._dfs(node, prefix)

    def get_suggestions(self, word):
        suggestions = self.autocomplete(word)
        distances = {}
        for suggestion in suggestions:
            distance = self._levenshtein_distance(word, suggestion)
            distances[suggestion] = distance
        sorted_suggestions = sorted(distances.keys(), key=lambda x: distances[x])
        return sorted_suggestions[:10]

    def _levenshtein_distance(self, s, t):
        if not s:
            return len(t)
        if not t:
            return len(s)
        if s[0] == t[0]:
            return self._levenshtein_distance(s[1:], t[1:])
        substitution = self._levenshtein_distance(s[1:], t[1:])
        deletion = self._levenshtein_distance(s[1:], t)
        insertion = self._levenshtein_distance(s, t[1:])
        return 1 + min(substitution, deletion, insertion)


# Load words from text file
with open('english_words.txt', 'r') as f:
    word_list = f.read().splitlines()

# Initialize Trie
trie = Trie()

# Insert words into Trie
for word in word_list:
    trie.insert(word.lower())

# Initialize GUI
root = tk.Tk()
root.title("Spell Checker and Autocomplete")

# Define event handlers
def check_word():
    user_input = entry.get()
    if trie.search(user_input.lower()):
        result.config(text=f"{user_input} is a valid word.")
    else:
        suggestions = trie.get_suggestions(user_input.lower())
        if suggestions:
            result.config(text="Did you mean:")
            for i, suggestion in enumerate(suggestions):
                suggestion_label = tk.Label(frame, text=f"{i+1}. {suggestion}")
                suggestion_label.grid(row=i+1, column=0, sticky="w")
        else:
            result.config(text=f"No suggestions found for {user_input}.")

def clear_results():
    for widget in frame.winfo_children():
        widget.destroy()
    result.config(text="")

# Define GUI layout
label = tk.Label(root, text="Enter a word or prefix:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Check", command=check_word)
button.pack()

result = tk.Label(root, text="")
result.pack()

frame = tk.Frame(root)
frame.pack()

clear_button = tk.Button(root, text="Clear Results", command=clear_results)
clear_button.pack()

root.mainloop()