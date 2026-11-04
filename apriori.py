"""
Программа для поиска частых наборов объектов с использованием алгоритма Apriori
"""

import csv
import time
from itertools import combinations
from collections import defaultdict
from typing import List, Set, Tuple, Dict


class Apriori:
    def __init__(self, min_support: float, sort_by: str = 'support'):
        """
        Инициализация алгоритма Apriori

        Args:
            min_support: Минимальный порог поддержки (от 0 до 1)
            sort_by: Способ сортировки результатов ('support' или 'lexicographic')
        """
        self.min_support = min_support
        self.sort_by = sort_by
        self.transactions = []
        self.frequent_itemsets = {}
        self.item_support = {}

    def load_data(self, filename: str, encoding: str = 'windows-1251'):
        """Загрузка данных из CSV файла"""
        self.transactions = []
        with open(filename, 'r', encoding=encoding) as f:
            for line in f:
                line = line.strip()
                if line:
                    # Транзакция состоит из товаров, разделенных запятыми
                    items = [item.strip() for item in line.split(',') if item.strip()]
                    if items:
                        self.transactions.append(set(items))
        return len(self.transactions)

    def get_support(self, itemset: frozenset) -> float:
        """Вычисление поддержки для набора объектов"""
        count = sum(1 for transaction in self.transactions if itemset.issubset(transaction))
        return count / len(self.transactions)

    def get_frequent_1_itemsets(self) -> Dict[frozenset, float]:
        """Получение частых 1-наборов"""
        item_counts = defaultdict(int)

        for transaction in self.transactions:
            for item in transaction:
                item_counts[item] += 1

        frequent_items = {}
        min_count = self.min_support * len(self.transactions)

        for item, count in item_counts.items():
            support = count / len(self.transactions)
            if support >= self.min_support:
                frequent_items[frozenset([item])] = support

        return frequent_items

    def generate_candidates(self, frequent_itemsets: List[frozenset], k: int) -> Set[frozenset]:
        """Генерация кандидатов размера k из частых наборов размера k-1"""
        candidates = set()
        frequent_list = list(frequent_itemsets)

        for i in range(len(frequent_list)):
            for j in range(i + 1, len(frequent_list)):
                union = frequent_list[i] | frequent_list[j]
                if len(union) == k:
                    candidates.add(union)

        return candidates

    def prune_candidates(self, candidates: Set[frozenset],
                        prev_frequent: Set[frozenset], k: int) -> Set[frozenset]:
        """Отсечение кандидатов, у которых не все подмножества частые"""
        pruned = set()

        for candidate in candidates:
            # Проверяем все подмножества размера k-1
            subsets = [frozenset(s) for s in combinations(candidate, k - 1)]
            if all(subset in prev_frequent for subset in subsets):
                pruned.add(candidate)

        return pruned

    def run(self) -> Dict[frozenset, float]:
        """Выполнение алгоритма Apriori"""
        start_time = time.time()

        # Шаг 1: Найти частые 1-наборы
        self.frequent_itemsets = self.get_frequent_1_itemsets()
        all_frequent = dict(self.frequent_itemsets)

        k = 2
        current_frequent = set(self.frequent_itemsets.keys())

        # Шаг 2: Итеративно находить частые k-наборы
        while current_frequent:
            # Генерация кандидатов
            candidates = self.generate_candidates(list(current_frequent), k)

            # Отсечение кандидатов
            candidates = self.prune_candidates(candidates, current_frequent, k)

            # Подсчет поддержки для кандидатов
            frequent_k = {}
            for candidate in candidates:
                support = self.get_support(candidate)
                if support >= self.min_support:
                    frequent_k[candidate] = support

            if not frequent_k:
                break

            all_frequent.update(frequent_k)
            current_frequent = set(frequent_k.keys())
            k += 1

        self.execution_time = time.time() - start_time
        return all_frequent

    def get_sorted_results(self, frequent_itemsets: Dict[frozenset, float]) -> List[Tuple[frozenset, float]]:
        """Сортировка результатов"""
        if self.sort_by == 'support':
            # Сортировка по убыванию поддержки
            return sorted(frequent_itemsets.items(), key=lambda x: x[1], reverse=True)
        else:
            # Лексикографическая сортировка
            return sorted(frequent_itemsets.items(),
                         key=lambda x: (len(x[0]), sorted(list(x[0]))))

    def print_results(self, frequent_itemsets: Dict[frozenset, float], max_items: int = None):
        """Вывод результатов"""
        sorted_results = self.get_sorted_results(frequent_itemsets)

        print(f"\nНайдено частых наборов: {len(sorted_results)}")
        print(f"Время выполнения: {self.execution_time:.4f} сек")
        print(f"Минимальная поддержка: {self.min_support * 100:.1f}%")
        print(f"Сортировка: {self.sort_by}")
        print("\nЧастые наборы объектов:")
        print("-" * 80)

        count = 0
        for itemset, support in sorted_results:
            if max_items and count >= max_items:
                print(f"... и еще {len(sorted_results) - max_items} наборов")
                break

            items = ', '.join(sorted(list(itemset)))
            print(f"{items:60} | Поддержка: {support * 100:6.2f}%")
            count += 1

    def get_itemsets_by_length(self, frequent_itemsets: Dict[frozenset, float]) -> Dict[int, int]:
        """Подсчет количества наборов по длине"""
        length_counts = defaultdict(int)
        for itemset in frequent_itemsets.keys():
            length_counts[len(itemset)] += 1
        return dict(length_counts)


def main():
    """Основная функция для демонстрации работы"""
    import sys

    if len(sys.argv) < 2:
        print("Использование: python apriori.py <min_support> [sort_by]")
        print("  min_support: минимальная поддержка в процентах (например, 5 для 5%)")
        print("  sort_by: 'support' (по умолчанию) или 'lexicographic'")
        sys.exit(1)

    min_support = float(sys.argv[1]) / 100
    sort_by = sys.argv[2] if len(sys.argv) > 2 else 'support'

    # Создание и запуск алгоритма
    apriori = Apriori(min_support=min_support, sort_by=sort_by)

    print(f"Загрузка данных из baskets.csv...")
    num_transactions = apriori.load_data('baskets.csv')
    print(f"Загружено транзакций: {num_transactions}")

    print(f"\nЗапуск алгоритма Apriori...")
    frequent_itemsets = apriori.run()

    # Вывод результатов
    apriori.print_results(frequent_itemsets, max_items=50)

    # Статистика по длинам наборов
    length_stats = apriori.get_itemsets_by_length(frequent_itemsets)
    print("\n" + "=" * 80)
    print("Распределение по длине наборов:")
    for length in sorted(length_stats.keys()):
        print(f"  Длина {length}: {length_stats[length]} наборов")


if __name__ == "__main__":
    main()
