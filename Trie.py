class NodeTrie:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word_count = 0


class PrefixTree:
    def __init__(self):
        self.root = NodeTrie()
        self.total_words = 0

    def add(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = NodeTrie()
            node = node.children[ch]

        if not node.is_end_of_word:
            self.total_words += 1
            node.word_count += 1
        node.is_end_of_word = True

    def suggest(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        return self._collect_words(node, prefix)

    def _collect_words(self, node, current):
        results = []
        if node.is_end_of_word:
            results.append(current)
        for ch, child in node.children.items():
            results.extend(self._collect_words(child, current + ch))
        return results

    def total_words_count(self):
        return self.total_words

    def has_prefix(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def contains(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end_of_word


def load_words_from_file(filename):
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                w = line.strip()
                if w:
                    words.append(w)
        return words
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []


def basic_test():
    print("=== TESTE BÁSICO ===")
    tree = PrefixTree()
    sample = ["apple", "banana", "apricot", "app", "appetizer", "bat", "ball", "batman"]

    for w in sample:
        tree.add(w)

    print("Número total de palavras na Trie:", tree.total_words_count())

    pref = "app"
    sug = tree.suggest(pref)
    print(f"Palavras que começam com '{pref}': {sug}")

    print(f"\nTestes adicionais:")
    print(f"Existe 'apple'? {tree.contains('apple')}")
    print(f"Existe 'appl'? {tree.contains('appl')}")
    print(f"Existe palavra com prefixo 'ba'? {tree.has_prefix('ba')}")


def file_test():
    print("\n=== TESTE COM ARQUIVO GRANDE ===")
    filename = "outputTP1.txt"
    words = load_words_from_file(filename)

    if not words:
        print("Nenhuma palavra carregada. Verifique o arquivo.")
        return

    print(f"Carregadas {len(words)} palavras do arquivo.")
    tree = PrefixTree()

    print("Inserindo palavras na Trie...")
    for i, w in enumerate(words):
        tree.add(w)
        if (i + 1) % 1000 == 0:
            print(f"Inseridas {i + 1} palavras...")

    print(f"\nNúmero total de palavras na Trie: {tree.total_words_count()}")

    while True:
        print("\n--- SISTEMA DE AUTOCOMPLETE ---")
        prefix = input("Digite um prefixo para buscar (ou 'sair' para terminar): ").strip().lower()

        if prefix == 'sair':
            break

        if not prefix:
            continue

        suggestions = tree.suggest(prefix)
        print(f"\nPalavras que começam com '{prefix}':")
        print(f"Encontradas {len(suggestions)} sugestões:")

        for i, pw in enumerate(suggestions[:20]):
            print(f"  {i + 1}. {pw}")

        if len(suggestions) > 20:
            print(f"  ... e mais {len(suggestions) - 20} palavras")


def performance_test(tree, test_prefixes):
    print("\n=== TESTE DE PERFORMANCE ===")
    import time
    for p in test_prefixes:
        start = time.time()
        res = tree.suggest(p)
        end = time.time()
        print(f"Prefix: '{p}' -> {len(res)} resultados em {end - start:.6f} segundos")
        if res:
            print(f"  Exemplos: {res[:3]}")


if __name__ == "__main__":
    basic_test()
    file_test()