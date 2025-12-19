"""
Проверка Example 1 - Divorce Arrangement детально
"""

# Оценки из Table 1
items = ["Retirement", "House", "Cottage", "Portfolio", "Other"]
a_d = [50, 20, 15, 10, 5]  
b_d = [40, 30, 10, 10, 10]

print("Example 1: Divorce Arrangement")
print("="*60)
print("\nОценки:")
for i, item in enumerate(items):
    print(f"{item:12s}: A={a_d[i]:2d}, B={b_d[i]:2d}")

total_a = sum(a_d)
total_b = sum(b_d)
print(f"\nВсего:        A={total_a}, B={total_b}")
print(f"50% для каждого: A≥{total_a/2:.2f}, B≥{total_b/2:.2f}")

print("\n" + "="*60)
print("Решение из статьи (AW):")
print("="*60)
print("Ann (A) получает:")
print("  - Cottage целиком (15)")
print("  - 5/6 Retirement (5/6 * 50 = 41.67)")
print("  Итого: 56.67")
print("\nBen (B) получает:")
print("  - Portfolio целиком (10)")
print("  - House целиком (30)")
print("  - Other целиком (10)")
print("  - 1/6 Retirement (1/6 * 40 = 6.67)")
print("  Итого: 56.67")

# Проверка
ann_gain = 15 + (5/6) * 50
ben_gain = 10 + 30 + 10 + (1/6) * 40
print(f"\nПроверка: Ann={ann_gain:.2f}, Ben={ben_gain:.2f}")

print("\n" + "="*60)
print("Поиск всех равноценных решений:")
print("="*60)

# Будем искать решения где делится максимум 1 предмет
# Для каждого предмета i пробуем его делить, остальные распределяем полностью

solutions = []

for split_idx in range(5):
    # Пробуем делить предмет split_idx
    # Остальные предметы распределяем всеми возможными способами
    
    from itertools import product
    other_indices = [i for i in range(5) if i != split_idx]
    
    for assignment in product([0, 1], repeat=4):
        # assignment[j] = 1 означает что предмет other_indices[j] идет A
        
        # Выигрыш A от целых предметов
        ga_whole = sum(a_d[other_indices[j]] * assignment[j] for j in range(4))
        # Выигрыш B от целых предметов
        gb_whole = sum(b_d[other_indices[j]] * (1 - assignment[j]) for j in range(4))
        
        # Решаем для x (доля split_idx для A):
        # ga_whole + x * a_d[split_idx] = gb_whole + (1-x) * b_d[split_idx]
        # ga_whole + x * a_d[split_idx] = gb_whole + b_d[split_idx] - x * b_d[split_idx]
        # x * (a_d[split_idx] + b_d[split_idx]) = gb_whole + b_d[split_idx] - ga_whole
        
        denom = a_d[split_idx] + b_d[split_idx]
        numer = gb_whole + b_d[split_idx] - ga_whole
        
        if denom > 0:
            x = numer / denom
            
            if 0 <= x <= 1:
                gain = ga_whole + x * a_d[split_idx]
                
                if gain >= total_a / 2 and gain >= total_b / 2:
                    # Формируем полное распределение
                    full_assignment = list(assignment)
                    full_assignment.insert(split_idx, x)
                    
                    solutions.append((split_idx, full_assignment, gain))

print(f"Найдено {len(solutions)} равноценных решений:\n")

for idx, (split_idx, assignment, gain) in enumerate(solutions, 1):
    print(f"{idx}. Делится: {items[split_idx]}")
    print(f"   Выигрыш: {gain:.2f}")
    print(f"   A получает:")
    
    for i in range(5):
        if i == split_idx:
            if assignment[i] > 0:
                print(f"     - {assignment[i]:.4f} × {items[i]} = {assignment[i] * a_d[i]:.2f}")
        else:
            # Найти индекс в assignment
            idx_in_assign = i if i < split_idx else i - 1
            if assignment[idx_in_assign] == 1:
                print(f"     - {items[i]} целиком = {a_d[i]}")
    
    print(f"   B получает:")
    for i in range(5):
        if i == split_idx:
            if assignment[i] < 1:
                print(f"     - {1-assignment[i]:.4f} × {items[i]} = {(1-assignment[i]) * b_d[i]:.2f}")
        else:
            idx_in_assign = i if i < split_idx else i - 1
            if assignment[idx_in_assign] == 0:
                print(f"     - {items[i]} целиком = {b_d[i]}")
    print()

# Проверяем решение из статьи
print("="*60)
print("Решение из статьи соответствует варианту:")
for idx, (split_idx, assignment, gain) in enumerate(solutions, 1):
    if split_idx == 0:  # Retirement
        x_ret = assignment[0]
        # A получает Cottage (index 2)
        has_cottage = False
        for i, val in enumerate(assignment[1:], 1):
            if i == 2 and val == 1:
                has_cottage = True
        
        if has_cottage and abs(x_ret - 5/6) < 0.01:
            print(f"Вариант #{idx}")
            break
