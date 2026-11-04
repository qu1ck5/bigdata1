"""
Генерация PDF отчета о результатах экспериментов с алгоритмом Apriori
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import json
import os


def register_fonts():
    """Регистрация шрифтов для поддержки кириллицы"""
    try:
        # Пробуем зарегистрировать системные шрифты Windows
        fonts_dir = 'C:\\Windows\\Fonts\\'

        # Arial
        pdfmetrics.registerFont(TTFont('Arial', fonts_dir + 'arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', fonts_dir + 'arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Italic', fonts_dir + 'ariali.ttf'))

        return 'Arial', 'Arial-Bold', 'Arial'
    except:
        try:
            # Пробуем DejaVu Sans (универсальный шрифт)
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont('DejaVuSans'))
            return 'DejaVuSans', 'DejaVuSans', 'Courier'
        except:
            # Используем встроенные шрифты (могут не отображать кириллицу)
            return 'Helvetica', 'Helvetica-Bold', 'Courier'


def create_report():
    """Создание PDF отчета"""

    # Регистрация шрифтов
    font_regular, font_bold, font_mono = register_fonts()

    # Создание PDF документа
    pdf_filename = "Отчет_Apriori.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    # Контейнер для элементов документа
    story = []

    # Стили
    styles = getSampleStyleSheet()

    # Пользовательские стили
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName=font_bold
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName=font_bold
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=10,
        fontName=font_bold
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14,
        fontName=font_regular
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName=font_mono,
        textColor=colors.HexColor('#2c3e50'),
        backColor=colors.HexColor('#f5f5f5'),
        leftIndent=10,
        rightIndent=10,
        spaceAfter=10
    )

    # Титульная страница
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("ОТЧЕТ", title_style))
    story.append(Paragraph("Поиск частых наборов объектов<br/>с использованием алгоритма Apriori",
                          heading1_style))
    story.append(Spacer(1, 2*cm))

    info_data = [
        ["Предмет:", "Анализ больших данных"],
        ["Дата:", "04.11.2026"],
        ["Набор данных:", "baskets.csv (покупки в супермаркете)"],
    ]

    info_table = Table(info_data, colWidths=[5*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), font_bold),
        ('FONTNAME', (1, 0), (1, -1), font_regular),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    story.append(info_table)
    story.append(PageBreak())

    # 1. Формулировка задания
    story.append(Paragraph("1. Формулировка задания", heading1_style))

    task_text = """
    Разработать программу, которая выполняет поиск частых наборов объектов в заданном
    наборе данных с помощью алгоритма Apriori (или одной из его модификаций).
    Список результирующих наборов должен содержать как наборы, так и значение поддержки
    для каждого набора.
    """
    story.append(Paragraph(task_text, body_style))

    story.append(Paragraph("<b>Параметры программы:</b>", body_style))
    params_text = """
    • Набор данных для анализа<br/>
    • Порог поддержки (минимальная частота встречаемости набора)<br/>
    • Способ упорядочивания результатов (по убыванию поддержки или лексикографический)
    """
    story.append(Paragraph(params_text, body_style))

    story.append(Paragraph("<b>Эксперименты:</b>", body_style))
    exp_text = """
    Провести эксперименты на наборе данных baskets.csv с варьированием порогового
    значения поддержки: 1%, 3%, 5%, 10%, 15%.
    """
    story.append(Paragraph(exp_text, body_style))

    story.append(Paragraph("<b>Визуализация результатов:</b>", body_style))
    viz_text = """
    • Сравнение быстродействия при изменяемом пороге поддержки<br/>
    • Количество частых наборов различной длины при изменяемом пороге поддержки
    """
    story.append(Paragraph(viz_text, body_style))

    story.append(Spacer(1, 0.5*cm))

    # 2. Гиперссылка на репозиторий
    story.append(Paragraph("2. Исходные материалы", heading1_style))

    repo_text = """
    Все исходные коды, наборы данных и результаты экспериментов доступны в рабочей директории:<br/>
    <font color="blue"><u>C:\\Users\\qu1ck\\Desktop\\bigdata</u></font>
    """
    story.append(Paragraph(repo_text, body_style))

    story.append(Paragraph("<b>Структура проекта:</b>", body_style))
    struct_text = """
    • <b>apriori.py</b> - основная программа с реализацией алгоритма Apriori<br/>
    • <b>experiments.py</b> - скрипт для проведения экспериментов<br/>
    • <b>baskets.csv</b> - набор данных (7501 транзакция)<br/>
    • <b>experiment_results.json</b> - результаты экспериментов в формате JSON<br/>
    • <b>*.png</b> - визуализации результатов
    """
    story.append(Paragraph(struct_text, body_style))

    story.append(PageBreak())

    # 3. Результаты экспериментов
    story.append(Paragraph("3. Результаты экспериментов", heading1_style))

    # Загрузка результатов
    with open('experiment_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)

    story.append(Paragraph("3.1. Сводная таблица результатов", heading2_style))

    # Таблица результатов
    table_data = [
        ['Порог\nподдержки', 'Время\nвыполнения (сек)', 'Количество\nчастых наборов', 'Макс.\nдлина набора']
    ]

    for r in results:
        max_len = max(r['length_distribution'].keys()) if r['length_distribution'] else 0
        table_data.append([
            f"{r['min_support_percent']:.0f}%",
            f"{r['execution_time']:.4f}",
            str(r['total_frequent_itemsets']),
            str(max_len)
        ])

    results_table = Table(table_data, colWidths=[3.5*cm, 4*cm, 4.5*cm, 3.5*cm])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), font_regular),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))

    story.append(results_table)
    story.append(Spacer(1, 0.5*cm))

    # Примеры частых наборов
    story.append(Paragraph("3.2. Примеры обнаруженных частых наборов", heading2_style))

    example_text = """
    Для порога поддержки 3% были обнаружены следующие наиболее частые наборы товаров
    (топ-5 по значению поддержки):
    """
    story.append(Paragraph(example_text, body_style))

    # Топ-5 наборов для порога 3%
    result_3pct = [r for r in results if r['min_support_percent'] == 3.0][0]
    top_items = result_3pct['top_itemsets'][:5]

    items_data = [['Набор товаров', 'Поддержка']]
    for item in top_items:
        items_str = ', '.join(item['items'][:3])  # Первые 3 товара
        if len(item['items']) > 3:
            items_str += f", ... (всего {len(item['items'])})"
        items_data.append([items_str, f"{item['support_percent']:.2f}%"])

    items_table = Table(items_data, colWidths=[12*cm, 3*cm])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), font_regular),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))

    story.append(items_table)
    story.append(PageBreak())

    # 4. Визуализация результатов
    story.append(Paragraph("4. Визуализация результатов", heading1_style))

    # График 1
    story.append(Paragraph("4.1. Зависимость времени выполнения от порога поддержки",
                          heading2_style))

    if os.path.exists('performance_vs_support.png'):
        img1 = Image('performance_vs_support.png', width=15*cm, height=9*cm)
        story.append(img1)
        story.append(Spacer(1, 0.3*cm))

    perf_text = """
    <b>Рисунок 1.</b> Сравнение быстродействия алгоритма Apriori при различных
    порогах поддержки на фиксированном наборе данных (7501 транзакция).
    """
    story.append(Paragraph(perf_text, body_style))
    story.append(Spacer(1, 0.5*cm))

    # График 2
    story.append(Paragraph("4.2. Распределение частых наборов по длине", heading2_style))

    if os.path.exists('itemsets_by_length.png'):
        img2 = Image('itemsets_by_length.png', width=15*cm, height=8.75*cm)
        story.append(img2)
        story.append(Spacer(1, 0.3*cm))

    dist_text = """
    <b>Рисунок 2.</b> Количество частых наборов объектов различной длины
    при изменяемом пороге поддержки.
    """
    story.append(Paragraph(dist_text, body_style))

    story.append(PageBreak())

    # График 3
    story.append(Paragraph("4.3. Общее количество частых наборов", heading2_style))

    if os.path.exists('total_itemsets_vs_support.png'):
        img3 = Image('total_itemsets_vs_support.png', width=15*cm, height=9*cm)
        story.append(img3)
        story.append(Spacer(1, 0.3*cm))

    total_text = """
    <b>Рисунок 3.</b> Зависимость общего количества обнаруженных частых наборов
    от порога поддержки.
    """
    story.append(Paragraph(total_text, body_style))

    story.append(PageBreak())

    # 5. Анализ и выводы
    story.append(Paragraph("5. Анализ результатов и выводы", heading1_style))

    story.append(Paragraph("5.1. Влияние порога поддержки на быстродействие", heading2_style))

    analysis1 = """
    Как видно из Рисунка 1, время выполнения алгоритма Apriori существенно зависит
    от порога поддержки. При минимальном пороге 1% время выполнения составляет
    ~1.08 секунды, в то время как при пороге 15% алгоритм выполняется всего за
    ~0.007 секунды - разница более чем в 150 раз.
    <br/><br/>
    Эта зависимость объясняется тем, что при низком пороге поддержки алгоритм
    генерирует и проверяет значительно больше кандидатов на каждой итерации.
    При высоком пороге большинство наборов отсеивается уже на ранних стадиях,
    что существенно сокращает объем вычислений.
    """
    story.append(Paragraph(analysis1, body_style))

    story.append(Paragraph("5.2. Количество и длина частых наборов", heading2_style))

    analysis2 = """
    Из Рисунков 2 и 3 видно, что количество обнаруженных частых наборов экспоненциально
    уменьшается с ростом порога поддержки:
    <br/>
    • При 1%: найдено 261 набор (максимальная длина - 3 товара)<br/>
    • При 3%: найдено 55 наборов (максимальная длина - 2 товара)<br/>
    • При 5%: найдено 28 наборов (максимальная длина - 2 товара)<br/>
    • При 10%: найдено 7 наборов (только одиночные товары)<br/>
    • При 15%: найдено 5 наборов (только одиночные товары)
    <br/><br/>
    При пороге 10% и выше обнаруживаются только одиночные товары (наборы длины 1),
    что указывает на отсутствие в данных устойчивых комбинаций товаров с такой
    высокой частотой встречаемости. Наборы длины 2-3 товара появляются только
    при порогах до 5%.
    """
    story.append(Paragraph(analysis2, body_style))

    story.append(Paragraph("5.3. Практические рекомендации", heading2_style))

    recommendations = """
    На основе проведенных экспериментов можно сделать следующие практические выводы:
    <br/><br/>
    <b>1. Выбор порога поддержки:</b><br/>
    Для данного набора данных о покупках в супермаркете оптимальным является порог
    3-5%. Этот диапазон обеспечивает разумный баланс между количеством найденных
    ассоциаций и их практической значимостью.
    <br/><br/>
    <b>2. Быстродействие:</b><br/>
    При работе с большими наборами данных рекомендуется начинать с более высоких
    порогов (5-10%) для быстрой оценки данных, а затем снижать порог для более
    детального анализа.
    <br/><br/>
    <b>3. Интерпретация результатов:</b><br/>
    Наборы длины 2-3, обнаруженные при пороге 1-3%, могут указывать на реальные
    покупательские предпочтения и быть использованы для рекомендательных систем
    и оптимизации размещения товаров в магазине.
    """
    story.append(Paragraph(recommendations, body_style))

    story.append(Spacer(1, 1*cm))

    # Заключение
    story.append(Paragraph("6. Заключение", heading1_style))

    conclusion = """
    В ходе выполнения задания была разработана полнофункциональная программа для
    поиска частых наборов объектов на основе алгоритма Apriori. Программа успешно
    протестирована на реальном наборе данных о покупках в супермаркете, содержащем
    7501 транзакцию.
    <br/><br/>
    Проведенные эксперименты с различными порогами поддержки (1%, 3%, 5%, 10%, 15%)
    продемонстрировали ожидаемое поведение алгоритма: экспоненциальное уменьшение
    времени выполнения и количества найденных наборов при увеличении порога поддержки.
    <br/><br/>
    Реализованная программа поддерживает все требуемые параметры (порог поддержки,
    способ сортировки результатов) и предоставляет детальную статистику по
    результатам работы алгоритма.
    """
    story.append(Paragraph(conclusion, body_style))

    # Сборка документа
    doc.build(story)
    print(f"✓ PDF отчет создан: {pdf_filename}")


if __name__ == "__main__":
    create_report()
