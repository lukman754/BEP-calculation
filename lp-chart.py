import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve

# Fungsi untuk mengambil input fungsi tujuan dan batasan secara dinamis
def get_input():
    print("Masukkan koefisien fungsi tujuan (cth: untuk 3x + 2y, masukkan 3 2): ")
    z = list(map(float, input().split()))
    
    constraints = []
    num_constraints = int(input("Masukkan jumlah batasan: "))
    
    for i in range(num_constraints):
        print(f"Masukkan koefisien batasan ke-{i+1} (cth: untuk 2x + y <= 4, masukkan 2 1 4): ")
        constraint = list(map(float, input().split()))
        constraints.append(constraint)
        
    return z, constraints

# Fungsi untuk menghitung dan menampilkan proses langkah demi langkah
def calculate_lp(z, constraints):
    x, y = symbols('x y')
    
    # Tampilkan fungsi tujuan
    print(f"\nFungsi tujuan: {z[0]}x + {z[1]}y")
    
    # Menyimpan solusi batasan
    solutions = []
    
    # Proses setiap batasan
    for i, constraint in enumerate(constraints):
        print(f"\nBatasan {i+1}: {constraint[0]}x + {constraint[1]}y <= {constraint[2]}")
        
        # Solusi perpotongan dengan sumbu x (y=0)
        x_intercept = constraint[2] / constraint[0] if constraint[0] != 0 else None
        if x_intercept is not None:
            print(f"  Perpotongan dengan sumbu x: x = {x_intercept:.2f}")
        
        # Solusi perpotongan dengan sumbu y (x=0)
        y_intercept = constraint[2] / constraint[1] if constraint[1] != 0 else None
        if y_intercept is not None:
            print(f"  Perpotongan dengan sumbu y: y = {y_intercept:.2f}")
        
        # Menyimpan batasan untuk plot grafik
        solutions.append((x_intercept, y_intercept))
    
    return solutions

# Fungsi untuk membuat plot grafik batasan dan daerah feasible
def plot_lp(solutions, constraints):
    x_vals = np.linspace(0, 10, 400)
    plt.figure(figsize=(8, 8))

    for i, constraint in enumerate(constraints):
        a, b, c = constraint
        y_vals = (c - a * x_vals) / b
        plt.plot(x_vals, y_vals, label=f'Batasan {i+1}')
        
        # Garis putus-putus (untuk memperjelas daerah feasible)
        plt.fill_between(x_vals, y_vals, where=(y_vals >= 0), alpha=0.2)
    
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(True, which='both')

    plt.legend()
    plt.title("Grafik Linear Programming")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

# Main function
def main():
    z, constraints = get_input()
    solutions = calculate_lp(z, constraints)
    plot_lp(solutions, constraints)

if __name__ == "__main__":
    main()
