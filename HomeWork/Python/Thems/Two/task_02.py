
boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Liza', 'Kira', 'Emma', 'Trisha']

if len(boys) != len(girls):
    print("Внимание, кто-то может остаться без пары.")
else:
    boys_sorted = sorted(boys)
    girls_sorted = sorted(girls)

    print("Идеальные пары:")
    for boy, girl in zip(boys_sorted, girls_sorted):
        print(f"{boy} и {girl}")
