import json
import csv

def read_users(file_path):
    """Чтение пользователей из JSON файла"""
    with open(file_path, 'r', encoding='utf-8') as file:
        users_data = json.load(file)
    
    # Отбираем только нужные поля для каждого пользователя
    cleaned_users = []
    for user in users_data:
        cleaned_user = {
            'name': user.get('name', ''),
            'gender': user.get('gender', ''),
            'address': user.get('address', ''),
            'age': user.get('age', 0)
        }
        cleaned_users.append(cleaned_user)
    
    return cleaned_users

def read_books(file_path):
    """Чтение книг из CSV файла"""
    books = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Создаём словарь только с нужными полями
            book = {
                'title': row.get('Title', ''),
                'author': row.get('Author', ''),
                'pages': int(row.get('Pages', 0)),
                'genre': row.get('Genre', '')
            }
            books.append(book)
    return books

def distribute_books(users, books):
    """Распределение книг между пользователями максимально равномерно"""
    num_users = len(users)
    num_books = len(books)
    
    # Расчёт базового количества книг на пользователя
    base_books_per_user = num_books // num_users
    remaining_books = num_books % num_users
    
    # Распределяем книги
    book_index = 0
    for i, user in enumerate(users):
        # Каждому пользователю базовое количество книг
        books_for_user = base_books_per_user
        
        # Первым пользователям добавляем по одной книге из остатка
        if i < remaining_books:
            books_for_user += 1
        
        # Добавляем книги пользователю
        user['books'] = books[book_index:book_index + books_for_user]
        book_index += books_for_user
    
    return users

def save_result(users, file_path):
    """Сохранение результата в JSON файл"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

def main():
    """Основная функция"""
    try:
        # Читаем данные из файлов
        print("Чтение данных из файлов...")
        users = read_users('users.json')
        books = read_books('books.csv')
        
        print(f"Загружено пользователей: {len(users)}")
        print(f"Загружено книг: {len(books)}")
        
        # Проверяем структуру данных
        print("\nПример структуры пользователя:")
        print(json.dumps(users[0], indent=2, ensure_ascii=False))
        
        print("\nПример структуры книги:")
        print(json.dumps(books[0], indent=2, ensure_ascii=False))
        
        # Распределяем книги
        print("\nРаспределение книг...")
        result = distribute_books(users, books)
        
        # Сохраняем результат
        print("Сохранение результата...")
        save_result(result, 'result.json')
        
        print("Готово! Результат сохранён в файл result.json")
        
        # Выводим статистику
        print("\nСтатистика распределения:")
        for user in result:
            print(f"{user['name']}: {len(user['books'])} книг")
            
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()