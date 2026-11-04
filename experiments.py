"""
Скрипт для проведения экспериментов с алгоритмом Apriori
"""

import json
import time
from apriori import Apriori
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Для работы без GUI


def run_experiments():
    """Проведение экспериментов с различными порогами поддержки"""

    support_thresholds = [0.01, 0.03, 0.05, 0.10, 0.15]
    results = []

    print("Начало экспериментов...")
    print("=" * 80)

    for min_support in support_thresholds:
        print(f"\nЭксперимент с минимальной поддержкой {min_support * 100}%")
        print("-" * 80)

        # Создание и запуск алгоритма
        apriori = Apriori(min_support=min_support, sort_by='support')

        # Загрузка данных
        num_transactions = apriori.load_data('baskets.csv')

        # Запуск алгоритма
        start_time = time.time()
        frequent_itemsets = apriori.run()
        execution_time = time.time() - start_time

        # Получение статистики по длинам наборов
        length_stats = apriori.get_itemsets_by_length(frequent_itemsets)

        # Сохранение результатов
        result = {
            'min_support': min_support,
            'min_support_percent': min_support * 100,
            'num_transactions': num_transactions,
            'execution_time': execution_time,
            'total_frequent_itemsets': len(frequent_itemsets),
            'length_distribution': length_stats,
            'top_itemsets': []
        }

        # Сохранение топ-10 наборов
        sorted_itemsets = apriori.get_sorted_results(frequent_itemsets)
        for itemset, support in sorted_itemsets[:10]:
            result['top_itemsets'].append({
                'items': list(itemset),
                'support': support,
                'support_percent': support * 100
            })

        results.append(result)

        # Вывод результатов
        print(f"Количество транзакций: {num_transactions}")
        print(f"Время выполнения: {execution_time:.4f} сек")
        print(f"Найдено частых наборов: {len(frequent_itemsets)}")
        print(f"Распределение по длине:")
        for length in sorted(length_stats.keys()):
            print(f"  Длина {length}: {length_stats[length]} наборов")

    # Сохранение результатов в JSON
    with open('experiment_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("Эксперименты завершены. Результаты сохранены в experiment_results.json")

    return results


def create_visualizations(results):
    """Создание визуализаций результатов"""

    print("\nСоздание визуализаций...")

    # Извлечение данных
    support_values = [r['min_support_percent'] for r in results]
    execution_times = [r['execution_time'] for r in results]
    total_itemsets = [r['total_frequent_itemsets'] for r in results]

    # Настройка стиля
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

    # График 1: Быстродействие vs порог поддержки
    plt.figure(figsize=(10, 6))
    plt.plot(support_values, execution_times, marker='o', linewidth=2, markersize=8)
    plt.xlabel('Порог поддержки (%)', fontsize=12)
    plt.ylabel('Время выполнения (сек)', fontsize=12)
    plt.title('Зависимость времени выполнения от порога поддержки', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(support_values)

    # Добавление значений на график
    for x, y in zip(support_values, execution_times):
        plt.annotate(f'{y:.3f}s', (x, y), textcoords="offset points",
                    xytext=(0,10), ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('performance_vs_support.png', dpi=300, bbox_inches='tight')
    print("✓ Сохранен график: performance_vs_support.png")
    plt.close()

    # График 2: Количество частых наборов различной длины
    plt.figure(figsize=(12, 7))

    # Определение максимальной длины набора
    max_length = max(max(r['length_distribution'].keys()) for r in results)

    # Подготовка данных для каждого порога поддержки
    x = list(range(1, max_length + 1))
    width = 0.15
    x_pos = list(range(len(x)))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    for i, result in enumerate(results):
        counts = [result['length_distribution'].get(length, 0) for length in x]
        offset = (i - len(results)/2 + 0.5) * width
        plt.bar([p + offset for p in x_pos], counts, width,
               label=f"{result['min_support_percent']:.0f}%",
               color=colors[i], alpha=0.8)

    plt.xlabel('Длина набора объектов', fontsize=12)
    plt.ylabel('Количество наборов', fontsize=12)
    plt.title('Распределение частых наборов по длине при различных порогах поддержки',
             fontsize=14, fontweight='bold')
    plt.xticks(x_pos, x)
    plt.legend(title='Порог поддержки', fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('itemsets_by_length.png', dpi=300, bbox_inches='tight')
    print("✓ Сохранен график: itemsets_by_length.png")
    plt.close()

    # График 3: Общее количество частых наборов vs порог поддержки
    plt.figure(figsize=(10, 6))
    plt.plot(support_values, total_itemsets, marker='s', linewidth=2, markersize=8, color='#2ca02c')
    plt.xlabel('Порог поддержки (%)', fontsize=12)
    plt.ylabel('Количество частых наборов', fontsize=12)
    plt.title('Зависимость количества частых наборов от порога поддержки',
             fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(support_values)

    # Добавление значений на график
    for x, y in zip(support_values, total_itemsets):
        plt.annotate(f'{y}', (x, y), textcoords="offset points",
                    xytext=(0,10), ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('total_itemsets_vs_support.png', dpi=300, bbox_inches='tight')
    print("✓ Сохранен график: total_itemsets_vs_support.png")
    plt.close()

    print("\nВсе визуализации созданы успешно!")


def print_summary_table(results):
    """Вывод сводной таблицы результатов"""
    print("\n" + "=" * 80)
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("=" * 80)
    print(f"{'Порог':<10} {'Время (сек)':<15} {'Всего наборов':<20} {'Макс. длина':<15}")
    print("-" * 80)

    for r in results:
        max_len = max(r['length_distribution'].keys()) if r['length_distribution'] else 0
        print(f"{r['min_support_percent']:>6.1f}%   {r['execution_time']:>10.4f}     "
              f"{r['total_frequent_itemsets']:>12}        {max_len:>8}")

    print("=" * 80)


if __name__ == "__main__":
    # Проведение экспериментов
    results = run_experiments()

    # Вывод сводной таблицы
    print_summary_table(results)

    # Создание визуализаций
    create_visualizations(results)

    print("\n✓ Все эксперименты завершены!")
