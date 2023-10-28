import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import tempfile

async def generate_expense_chart(user_data):
    dates, costs = [], [], []
    for purchase in reversed(user_data['purchases']):
        dates.append(datetime.utcfromtimestamp(purchase['timestamp']))
        costs.append(purchase['cost'])

    fig, ax = plt.subplots()
    ax.plot_date(dates, costs, '-')
    ax.set_title('График истории расходов')
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    expense_chart_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.autofmt_xdate(rotation=45)
    plt.savefig(expense_chart_file.name, format='png')
    plt.close(fig)

    return expense_chart_file.name

async def generate_expense_chart(user_data):
    dates, costs = [], []
    for purchase in reversed(user_data['purchases']):
        dates.append(datetime.utcfromtimestamp(purchase['timestamp']))
        costs.append(purchase['cost'])

    fig, ax = plt.subplots()
    ax.plot_date(dates, costs, '-')
    ax.set_title('График истории расходов')
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    expense_chart_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.autofmt_xdate(rotation=45)
    plt.savefig(expense_chart_file.name, format='png')
    plt.close(fig)

    return expense_chart_file.name

async def generate_category_chart(user_data):
    category_expenses = {}
    for purchase in user_data['purchases']:
        category = purchase['category']
        cost = purchase['cost']
        category_expenses[category] = category_expenses.get(category, 0) + cost
    
    fig, ax = plt.subplots()
    ax.pie(category_expenses.values(), labels=category_expenses.keys(), autopct='%1.1f%%')
    ax.axis('equal')
    
    category_chart_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.autofmt_xdate(rotation=45)
    plt.savefig(category_chart_file.name, format='png')
    plt.close(fig)
    category_chart_file.close()

    return category_chart_file.name

async def generate_distribution_histogram(user_data):
    costs = [purchase['cost'] for purchase in user_data['purchases']]
    
    fig, ax = plt.subplots()
    ax.hist(costs, bins=10, edgecolor='black')
    ax.set_title('Распределение стоимости покупок')
    ax.set_xlabel('Стоимость')
    ax.set_ylabel('Количество покупок')
    
    distribution_hist_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.autofmt_xdate(rotation=45)
    plt.savefig(distribution_hist_file.name, format='png')
    plt.close(fig)
    distribution_hist_file.close()
    
    return distribution_hist_file.name

async def generate_cumulative_expense_chart(user_data):
    dates, cumulative_costs = [], []
    cumulative_cost = 0
    for purchase in sorted(user_data['purchases'], key=lambda x: x['timestamp']):
        cumulative_cost += purchase['cost']
        dates.append(datetime.utcfromtimestamp(purchase['timestamp']))
        cumulative_costs.append(cumulative_cost)
    
    fig, ax = plt.subplots()
    ax.plot_date(dates, cumulative_costs, '-')
    ax.set_title('График суммарных расходов по времени')
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    cumulative_expense_chart_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.autofmt_xdate(rotation=45)
    plt.savefig(cumulative_expense_chart_file.name, format='png')
    plt.close(fig)
    cumulative_expense_chart_file.close()
    
    return cumulative_expense_chart_file.name

async def generate_weekday_expense_chart(user_data):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_translations = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
    weekday_expenses = {weekday: 0 for weekday in weekdays}
    
    for purchase in user_data['purchases']:
        weekday = datetime.utcfromtimestamp(purchase['timestamp']).strftime('%A')
        weekday_expenses[weekday] += purchase['cost']
    
    fig, ax = plt.subplots()
    colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33A1', '#FFBD33', '#33FFBD', '#A133FF']
    ax.bar(weekdays, [weekday_expenses[weekday] for weekday in weekdays], color=colors)
    ax.set_title('Расходы по дням недели')
    ax.set_xticks(weekdays)
    ax.set_xticklabels([weekday_translations[weekday] for weekday in weekdays])
    
    
    weekday_expense_chart_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.autofmt_xdate(rotation=45)
    plt.savefig(weekday_expense_chart_file.name, format='png')
    plt.close(fig)
    weekday_expense_chart_file.close()
    
    return weekday_expense_chart_file.name

async def generate_average_expense_per_category_chart(user_data):
    category_expenses = {}
    category_counts = {}
    for purchase in user_data['purchases']:
        category = purchase['category']
        category_expenses[category] = category_expenses.get(category, 0) + purchase['cost']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    average_expenses = {category: category_expenses[category] / category_counts[category] for category in category_expenses}
    
    fig, ax = plt.subplots()
    ax.bar(average_expenses.keys(), average_expenses.values(), color='#A133FF')
    ax.set_title('Средние расходы по каждой категории')
    
    average_expense_per_category_chart_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.autofmt_xdate(rotation=45)
    plt.savefig(average_expense_per_category_chart_file.name, format='png')
    plt.close(fig)
    average_expense_per_category_chart_file.close()
    
    return average_expense_per_category_chart_file.name

charts = [
    ("График истории расходов", generate_expense_chart),
    ("График распределения категорий", generate_category_chart),
    ("График распределения стоимости покупок", generate_distribution_histogram),
    ("График суммарных расходов по времени", generate_cumulative_expense_chart),
    ("График расходов по дням недели", generate_weekday_expense_chart),
    ("График средних расходов по каждой категории", generate_average_expense_per_category_chart),
]