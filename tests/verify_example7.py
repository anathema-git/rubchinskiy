"""
Проверка Example 7 детально
"""

# Оценки
a_d = [17]  # item 0 делимый
b_d = [17]

a_w = [42, 37, 2, 2]  # items 1-4 неделимые
b_w = [45, 34, 2, 2]

print("Example 7: Fair Division")
print("="*60)
print("\nОценки:")
print(f"Item 0 (делимый): A={a_d[0]}, B={b_d[0]}")
print(f"Item 1: A={a_w[0]}, B={b_w[0]}")
print(f"Item 2: A={a_w[1]}, B={b_w[1]}")
print(f"Item 3: A={a_w[2]}, B={b_w[2]}")
print(f"Item 4: A={a_w[3]}, B={b_w[3]}")

print("\n" + "="*60)
print("Решение из статьи:")
print("="*60)
print("A получает: item2 (37) + 14.5/17 of item0")
print("B получает: item1 (45) + item3 (2) + item4 (2) + 2.5/17 of item0")

# Проверка статьи
ga_article = 37 + 14.5
gb_article = 45 + 2 + 2 + 2.5

print(f"\nВыигрыш A: {ga_article}")
print(f"Выигрыш B: {gb_article}")
print(f"Доля item0 для A: {14.5/17:.6f}")

print("\n" + "="*60)
print("Альтернативное решение:")
print("="*60)
print("A получает: item2 (37) + item3 (2) + item4 (2) + x·17")
print("B получает: item1 (45) + (1-x)·17")

# Решаем уравнение: 37 + 2 + 2 + 17x = 45 + 17(1-x)
# 41 + 17x = 45 + 17 - 17x
# 41 + 17x = 62 - 17x
# 34x = 21
# x = 21/34

x = 21 / 34
ga_alt = 37 + 2 + 2 + 17*x
gb_alt = 45 + 17*(1-x)

print(f"\nРешаем: 41 + 17x = 62 - 17x")
print(f"34x = 21")
print(f"x = {x:.6f}")
print(f"\nВыигрыш A: {ga_alt:.2f}")
print(f"Выигрыш B: {gb_alt:.2f}")

print("\n" + "="*60)
print("Проверим все возможные распределения неделимых:")
print("="*60)

# Все возможные распределения неделимых
from itertools import product

results = []
for sigma in product([0, 1], repeat=4):
    # Выигрыш от неделимых
    ga_ind = sum(a_w[i] * sigma[i] for i in range(4))
    gb_ind = sum(b_w[i] * (1-sigma[i]) for i in range(4))
    
    print(f"σ={sigma}: ga_ind={ga_ind}, gb_ind={gb_ind}")
    
    # Проверяем можно ли выровнять
    diff = ga_ind - gb_ind
    
    if diff > 17:
        # A слишком много впереди, даже отдав весь item0 не выровнять
        max_ga = ga_ind
        max_gb = gb_ind + 17
        if max_ga >= 50 and max_gb >= 50:
            results.append((sigma, max_ga, max_gb, 0.0))
            print(f"  → Пропорциональное (A впереди): ({max_ga:.2f}, {max_gb:.2f}), x=0.0")
    elif diff < -17:
        # B слишком много впереди
        max_ga = ga_ind + 17
        max_gb = gb_ind
        if max_ga >= 50 and max_gb >= 50:
            results.append((sigma, max_ga, max_gb, 1.0))
            print(f"  → Пропорциональное (B впереди): ({max_ga:.2f}, {max_gb:.2f}), x=1.0")
    else:
        # Можем выровнять
        # ga_ind + 17x = gb_ind + 17(1-x)
        # ga_ind + 17x = gb_ind + 17 - 17x
        # 34x = gb_ind + 17 - ga_ind
        x_eq = (gb_ind + 17 - ga_ind) / 34
        
        if 0 <= x_eq <= 1:
            gain_eq = ga_ind + 17 * x_eq
            if gain_eq >= 50:
                results.append((sigma, gain_eq, gain_eq, x_eq))
                print(f"  → Равноценное: ({gain_eq:.2f}, {gain_eq:.2f}), x={x_eq:.4f}")
        
        # Также добавляем крайние случаи
        # x=0: A получает только неделимые
        ga0 = ga_ind
        gb0 = gb_ind + 17
        if ga0 >= 50 and gb0 >= 50:
            results.append((sigma, ga0, gb0, 0.0))
            print(f"  → Пропорциональное (x=0): ({ga0:.2f}, {gb0:.2f})")
        
        # x=1: A получает все
        ga1 = ga_ind + 17
        gb1 = gb_ind
        if ga1 >= 50 and gb1 >= 50:
            results.append((sigma, ga1, gb1, 1.0))
            print(f"  → Пропорциональное (x=1): ({ga1:.2f}, {gb1:.2f})")

print(f"\nНайдено {len(results)} пропорциональных решений:")
for i, (sigma, ga, gb, x) in enumerate(results, 1):
    print(f"\n{i}. σ={sigma}, x={x:.4f}")
    print(f"   A: {ga:.2f}, B: {gb:.2f}")
    print(f"   A получает:", end="")
    for j in range(4):
        if sigma[j] == 1:
            print(f" item{j+1}", end="")
    if x > 0:
        print(f" + {x:.4f}·item0", end="")
    print()

# Ищем равноценные
equitable = [r for r in results if abs(r[1] - r[2]) < 0.01]
print(f"\n{'='*60}")
print(f"Из них равноценных: {len(equitable)}")
for i, (sigma, ga, gb, x) in enumerate(equitable, 1):
    print(f"\n{i}. σ={sigma}, x={x:.4f}")
    print(f"   Выигрыш: {ga:.2f} = {gb:.2f}")
    print(f"   A получает:", end="")
    for j in range(4):
        if sigma[j] == 1:
            print(f" item{j+1}", end="")
    if x > 0:
        print(f" + {x:.4f}·item0", end="")
    print()
