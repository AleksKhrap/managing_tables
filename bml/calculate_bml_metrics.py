import os
import re
from collections import defaultdict

RANKS = [
    (0, 'A'),
    (6, 'B'),
    (11, 'C'),
    (21, 'D'),
    (31, 'E'),
    (41, 'F')
]

def rank(complexity):
    for threshold, letter in reversed(RANKS):
        if complexity >= threshold:
            return letter

def calculate_bml_complexity(lines):
    complexity = 1  # стартовая сложность
    for line in lines:
        if any(k in line for k in ['act=', 'post-act=', 'fetch=', 'where=', 'nest=', 'if=', 'grants=']):
            complexity += 1
    return complexity

def analyze_bml_directory(directory):
    results = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.bml'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=directory)
                with open(full_path, encoding='utf-8') as f:
                    lines = f.readlines()

                label = extract_label(lines)
                complexity = calculate_bml_complexity(lines)
                letter = rank(complexity)
                results[rel_path].append((label, complexity, letter))
    return results

def extract_label(lines):
    for line in lines:
        m = re.search(r'base="([^"]+)"', line)
        if m:
            return m.group(1)
    return "(unknown)"

def print_results(results):
    block_count = 0
    total_complexity = 0
    print()
    for file, blocks in sorted(results.items()):
        print(f".\\{file}")
        for label, complexity, letter in blocks:
            print(f"    B 1:0 {label} - {letter} ({complexity})")
            block_count += 1
            total_complexity += complexity

    average = total_complexity / block_count if block_count else 0
    avg_letter = rank(average)
    print(f"\n{block_count} blocks analyzed.")
    print(f"Average complexity: {avg_letter} ({average:.1f})")

# Пример запуска
if __name__ == "__main__":
    import sys
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    results = analyze_bml_directory(target_dir)
    print_results(results)
