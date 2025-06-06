import os
import math
from antlr4 import *
from Python3Lexer import Python3Lexer

IGNORED_DIRS = {'venv', '__pycache__', 'forum', 'migrations', 'bml'}
IGNORED_FILES = {'manage.py', 'calculate_metrics.py', 'Python3Lexer.py', 'Python3Parser.py', 'Python3ParserListener.py',
                 'Python3LexerBase.py', 'Python3ParserBase.py', '__init__.py', 'radon.py', 'radon_graphics.py',
                 'calculate_metrics_v2.py', 'halstead_metrics.py'}

# Метрики Холстеда
class HalsteadMetrics:
    def __init__(self):
        self.operators = set()
        self.operands = set()
        self.N1 = 0  # операторов всего
        self.N2 = 0  # операндов всего

    def add_operator(self, op):
        self.operators.add(op)
        self.N1 += 1

    def add_operand(self, opd):
        self.operands.add(opd)
        self.N2 += 1

    def compute(self):
        n1 = len(self.operators)
        n2 = len(self.operands)
        N1 = self.N1
        N2 = self.N2
        n = n1 + n2
        N = N1 + N2
        V = N * (0 if n == 0 else math.log2(n))
        D = (n1 / 2) * (N2 / (n2 or 1))
        E = D * V
        L = 1 / D if D else 0

        return {
            'n1': n1, 'n2': n2, 'N1': N1, 'N2': N2,
            'Vocabulary': n, 'Length': N, 'Volume': V,
            'Difficulty': D, 'Effort': E, 'Quality Level': L
        }

def analyze_file(file_path, metrics: HalsteadMetrics):
    input_stream = FileStream(file_path, encoding='utf-8')   # Создание потока для чтения исходного кода файла
    lexer = Python3Lexer(input_stream)  # Лексический анализатор для Python 3 (генерируется с помощью ANTLR)
    tokens = CommonTokenStream(lexer)  # Создание потока токенов из лексера
    tokens.fill()  # Загружаем все токены в память

    # Проход по каждому токену для классификации его как операнд или оператор
    for token in tokens.tokens:
        if token.type in (Python3Lexer.NAME, Python3Lexer.NUMBER, Python3Lexer.STRING):
            metrics.add_operand(token.text)
        elif token.channel == Token.DEFAULT_CHANNEL:
            metrics.add_operator(token.text)

def walk_and_analyze(project_path):
    metrics = HalsteadMetrics()

    # Рекурсивный обход всех файлов и папок
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith('migrations')]
        for file in files:
            if file.endswith('.py') and file not in IGNORED_FILES:
                filepath = os.path.join(root, file)
                print(f"Analyzing: {filepath}")
                analyze_file(filepath, metrics)

    return metrics.compute()


if __name__ == "__main__":
    project_dir = "."
    result = walk_and_analyze(project_dir)
    print("\n📊 Halstead Metrics:")
    for k, v in result.items():
        print(f"{k:>20}: {v}")
