import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve

# Fungsi untuk menampilkan input dinamis dengan tampilan tabel di streamlit
def get_input():
    st.title("Kalkulator Linear Programming (Metode Grafik)")

    # Fungsi Tujuan
    st.header("Input Fungsi Tujuan")
    
    cols = st.columns(2)  # Buat dua kolom untuk input x dan y
    z_x = cols[0].number_input("Koefisien x", value=1.0, key="z_x", format="%g")
    z_y = cols[1].number_input("Koefisien y", value=1.0, key="z_y", format="%g")
    
    z = [z_x, z_y]

    num_constraints = st.number_input("Jumlah Batasan", min_value=1, max_value=5, step=1, value=2, key="num_constraints")

    # Input Batasan
    st.header("Input Batasan dalam Tabel")
    
    # Membuat tabel batasan dengan 3 kolom untuk setiap koefisien dan nilai batasan
    st.write("Masukkan Koefisien untuk x, y, dan Nilai Batasan di Tabel")
    constraint_cols = st.columns(3)  # Buat tiga kolom untuk tabel
    
    constraints = []
    # Menambahkan judul kolom
    constraint_cols[0].write("Koefisien x")
    constraint_cols[1].write("Koefisien y")
    constraint_cols[2].write("Nilai batasan (<=)")
    
    # Mengambil input batasan untuk setiap baris
    for i in range(num_constraints):
        with constraint_cols[0]:
            a = st.number_input(f"x{i+1}", value=1.0, key=f"a_{i}", format="%g")
        with constraint_cols[1]:
            b = st.number_input(f"y{i+1}", value=1.0, key=f"b_{i}", format="%g")
        with constraint_cols[2]:
            c = st.number_input(f"Batasan {i+1}", value=1.0, key=f"c_{i}", format="%g")
        
        constraints.append([a, b, c])
    
    return z, constraints

# Fungsi untuk menghitung dan menampilkan proses langkah demi langkah
def calculate_lp(z, constraints):
    x, y = symbols('x y')
    
    # Tampilkan fungsi tujuan
    st.subheader("Fungsi Tujuan")
    st.write(f"Fungsi tujuan: {z[0]}x + {z[1]}y")
    
    # Menyimpan solusi batasan
    solutions = []
    max_x = 0
    max_y = 0
    
    # Proses setiap batasan
    for i, constraint in enumerate(constraints):
        st.subheader(f"Batasan {i+1}")
        st.write(f"Batasan: {constraint[0]}x + {constraint[1]}y <= {constraint[2]}")
        
        # Menggunakan persamaan untuk eliminasi atau substitusi
        equation = Eq(constraint[0]*x + constraint[1]*y, constraint[2])
        st.write(f"Persamaan batasan: {constraint[0]}x + {constraint[1]}y = {constraint[2]}")
        
        # Solusi perpotongan dengan sumbu x (y=0)
        if constraint[1] != 0:  # Pastikan tidak ada pembagian dengan 0
            x_intercept = solve(equation.subs(y, 0), x)
            if x_intercept:
                x_intercept_value = x_intercept[0] if x_intercept else 0
                st.write(f"  Proses eliminasi untuk menemukan perpotongan dengan sumbu x (y = 0):")
                st.latex(f"{constraint[0]}x = {constraint[2]}")
                st.latex(f"x = {x_intercept_value:.2f}")
                st.write(f"  Perpotongan dengan sumbu x: x = {x_intercept_value:.2f}")
                max_x = max(max_x, x_intercept_value)
            else:
                x_intercept_value = 0
        else:
            x_intercept_value = 0  # Default jika tidak ada solusi valid
        
        # Solusi perpotongan dengan sumbu y (x=0)
        if constraint[0] != 0:  # Pastikan tidak ada pembagian dengan 0
            y_intercept = solve(equation.subs(x, 0), y)
            if y_intercept:
                y_intercept_value = y_intercept[0] if y_intercept else 0
                st.write(f"  Proses eliminasi untuk menemukan perpotongan dengan sumbu y (x = 0):")
                st.latex(f"{constraint[1]}y = {constraint[2]}")
                st.latex(f"y = {y_intercept_value:.2f}")
                st.write(f"  Perpotongan dengan sumbu y: y = {y_intercept_value:.2f}")
                max_y = max(max_y, y_intercept_value)
            else:
                y_intercept_value = 0
        else:
            y_intercept_value = 0  # Default jika tidak ada solusi valid
        
        # Menyimpan batasan untuk plot grafik
        solutions.append((x_intercept_value, y_intercept_value))
    
    return solutions, max_x, max_y

# Fungsi untuk membuat plot grafik batasan dan daerah feasible
def plot_lp(solutions, constraints, max_x, max_y):
    # Buat skala sumbu dinamis berdasarkan nilai maksimum
    x_vals = np.linspace(0, max(max_x, 10), 400)
    plt.figure(figsize=(8, 8))

    for i, constraint in enumerate(constraints):
        a, b, c = constraint
        # Pastikan tidak ada pembagian dengan 0
        if b != 0:
            y_vals = (c - a * x_vals) / b
            # Filter nilai tak hingga atau NaN
            y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
            plt.plot(x_vals, y_vals, label=f'Batasan {i+1}')
            plt.fill_between(x_vals, y_vals, where=(y_vals >= 0) & np.isfinite(y_vals), alpha=0.2)
        elif a != 0:
            # Handle vertical lines (x = constant)
            x_const = c / a
            plt.axvline(x=x_const, label=f'Batasan {i+1}', linestyle='--')
            plt.fill_betweenx([0, max(max_y, 10)], 0, x_const, alpha=0.2)
    
    plt.xlim(0, max(max_x, 10))
    plt.ylim(0, max(max_y, 10))
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, which='both')

    plt.legend()
    plt.title("Grafik Linear Programming")
    plt.xlabel("x")
    plt.ylabel("y")
    
    st.pyplot(plt)

# Main function for Streamlit app
def main():
    z, constraints = get_input()
    
    if st.button("Hitung dan Tampilkan Grafik"):
        solutions, max_x, max_y = calculate_lp(z, constraints)
        plot_lp(solutions, constraints, max_x, max_y)

if __name__ == "__main__":
    main()
