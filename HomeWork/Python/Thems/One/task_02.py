ticket = input("Введите номер билета (6 цифр): ")

first_half_sum = int(ticket[0]) + int(ticket[1]) + int(ticket[2])
second_half_sum = int(ticket[3]) + int(ticket[4]) + int(ticket[5])

if first_half_sum == second_half_sum:
    print("Счастливый билет")
else:
    print("Несчастливый билет")