file = open('file.txt', 'r+')

# Чтение данных из файла
data = file.read()
print(data)

# Запись данных в файл
file.write('Новые данные')

# Закрытие файла
file.close()