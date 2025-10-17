word = input("Введите слово: ")
length = len(word)

if length % 2 == 0:
    middle = word[length // 2 - 1:length // 2 + 1]
else:
    middle = word[length // 2]

print("Результат:", middle)
