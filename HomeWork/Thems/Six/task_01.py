import json

purchases = {}
with open('purchase_log.json', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        user_id = data.get('user_id')
        category = data.get('category')
        if user_id and category:
            purchases[user_id] = category

with open('visit_log__1_.csv', 'r', encoding='utf-8') as visit_file, \
        open('funnel.csv', 'w', encoding='utf-8') as funnel_file:
    funnel_file.write('user_id,source,category\n')

    header = visit_file.readline()

    for line in visit_file:
        parts = line.strip().split(',')
        if len(parts) != 2:
            continue
        user_id, source = parts

        if user_id in purchases:
            category = purchases[user_id]
            funnel_file.write(f'{user_id},{source},{category}\n')

print("Готово! Результат записан в funnel.csv")