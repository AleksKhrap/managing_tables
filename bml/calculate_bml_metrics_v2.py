import re
import os
import math

class HalsteadMetrics:
    def __init__(self):
        self.operators = []
        self.operands = []

    def add_operator(self, op):
        self.operators.append(op)

    def add_operand(self, opd):
        self.operands.append(opd)

    def compute_base(self):
        n1 = len(set(self.operators))
        n2 = len(set(self.operands))
        N1 = len(self.operators)
        N2 = len(self.operands)

        n = n1 + n2
        N = N1 + N2
        V = N * math.log2(n) if n > 0 else 0
        D = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        E = D * V
        L = 1 / D if D else 0

        return {
            'n1 (unique operators)': n1,
            'n2 (unique operands)': n2,
            'N1 (total operators)': N1,
            'N2 (total operands)': N2,
            'Vocabulary': n,
            'Length': N,
            'Volume': V,
            'Difficulty': D,
            'Effort': E,
            'Quality Level': L
        }

class ExtendedMetrics(HalsteadMetrics):
    def __init__(self):
        super().__init__()
        self.total_lines = 0        # LOC
        self.source_lines = 0       # SLOC
        self.logical_lines = 0      # LLOC
        self.cyclomatic = 1         # базовая цикломатическая сложность

    def analyze_line(self, line: str):
        stripped = line.strip()
        self.total_lines += 1

        if stripped == '' or stripped.startswith('<!--'):
            return

        self.source_lines += 1

        if re.match(r'<(set|block|location|groups?)\b', stripped):
            self.logical_lines += 1

        if any(k in stripped for k in ['act=', 'post-act=', 'fetch=', 'where=', 'nest=']):
            self.cyclomatic += 1

    def compute(self):
        base = self.compute_base()
        base.update({
            'LOC (total lines)': self.total_lines,
            'SLOC (source lines)': self.source_lines,
            'LLOC (logical lines)': self.logical_lines,
            'Cyclomatic Complexity': self.cyclomatic
        })
        return base

def tokenize_bml(content):
    """Разбор BML-файла на токены (операторы и операнды)"""
    tag_pattern = re.compile(r"<(/?)(\w+)")  # Захват открывающих и закрывающих тегов: <tag>, </tag>
    attr_pattern = re.compile(r'(\w+)="([^"]*)"')  # Захват атрибутов: key="value"

    operators = []
    operands = []

    # Теги (операторы) — сохраняем как <tag> или </tag>
    for tag_match in tag_pattern.finditer(content):
        is_close, tag = tag_match.groups()
        operators.append(f"</{tag}>" if is_close else f"<{tag}>")

    for attr_match in attr_pattern.finditer(content):
        attr, value = attr_match.groups()  # Атрибуты: ключ — оператор, значение — операнд
        operators.append(attr)
        operands.append(value)

    return operators, operands

def analyze_bml_file(path, metrics):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    for line in content.splitlines():
        metrics.analyze_line(line)

    operators, operands = tokenize_bml(content)
    for op in operators:
        metrics.add_operator(op)
    for opd in operands:
        metrics.add_operand(opd)

def analyze_bml_directory(directory):
    metrics = ExtendedMetrics()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".bml"):
                path = os.path.join(root, file)
                print(f"Analyzing: {path}")
                analyze_bml_file(path, metrics)
    return metrics.compute()


if __name__ == "__main__":
    import sys
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    results = analyze_bml_directory(target_dir)

    print("\n📊 BML Code Metrics")
    print("=" * 50)
    for k, v in results.items():
        print(f"{k:>30}: {v:.2f}" if isinstance(v, float) else f"{k:>30}: {v}")
