import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve

# Fungsi untuk menampilkan input dinamis dengan streamlit
def get_input():
    st.title("Kalkulator Linear Programming (Metode Grafik)")

    # Fungsi Tujuan
    st.header("Input Fungsi Tujuan")
    
    cols = st.columns(2)  # Buat dua kolom untuk input x dan y
    z_x = cols[0].number_input("Koefisien x", value=1.0, key="z_x", format="%.g")
    z_y = cols[1].number_input("Koefisien y", value=1.0, key="z_y", format="%.g")
    
    z = [z_x, z_y]

    num_constraints = st.number_input("Jumlah Batasan", min_value=1, max_value=5, step=1, value=2, key="num_constraints", format="%.g")

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
            a = st.number_input(f"x{i+1}", value=1.0, key=f"a_{i}", format="%.g")
        with constraint_cols[1]:
            b = st.number_input(f"y{i+1}", value=1.0, key=f"b_{i}", format="%.g")
        with constraint_cols[2]:
            c = st.number_input(f"Batasan {i+1}", value=1.0, key=f"c_{i}", format="%.g")
        
        constraints.append([a, b, c])
    
    return z, constraints

# Fungsi untuk menghitung dan menampilkan proses langkah demi langkah
# Fungsi untuk menghitung dan menampilkan proses langkah demi langkah
def calculate_lp(z, constraints):
    x, y = symbols('x y')
    
    # Tampilkan fungsi tujuan
    st.subheader("Fungsi Tujuan")
    st.write(f"Fungsi tujuan: {z[0]}x + {z[1]}y")
    
    # Menyimpan solusi batasan
    solutions = []
    
    # Proses setiap batasan
    for i, constraint in enumerate(constraints):
        st.subheader(f"Batasan {i+1}")
        st.write(f"Batasan: {constraint[0]}x + {constraint[1]}y <= {constraint[2]}")
        
        # Menggunakan persamaan untuk eliminasi atau substitusi
        equation = Eq(constraint[0]*x + constraint[1]*y, constraint[2])
        st.write(f"Persamaan batasan: {constraint[0]}x + {constraint[1]}y = {constraint[2]}")
        
        # Solusi perpotongan dengan sumbu x (y=0)
        if constraint[1] != 0:  # Pastikan koefisien y tidak 0
            x_intercept = solve(equation.subs(y, 0), x)
            if x_intercept and float(x_intercept[0]) != 0:
                st.write(f"  Proses eliminasi untuk menemukan perpotongan dengan sumbu x (y = 0):")
                st.latex(f"{constraint[0]}x = {constraint[2]}")
                st.latex(f"x = {float(x_intercept[0]):g}")
                st.write(f"  Perpotongan dengan sumbu x: x = {float(x_intercept[0]):g}")
        else:
            x_intercept = [None]  # Jika y=0, tidak ada intercept dengan x
        
        # Solusi perpotongan dengan sumbu y (x=0)
        if constraint[0] != 0:  # Pastikan koefisien x tidak 0
            y_intercept = solve(equation.subs(x, 0), y)
            if y_intercept and float(y_intercept[0]) != 0:
                st.write(f"  Proses eliminasi untuk menemukan perpotongan dengan sumbu y (x = 0):")
                st.latex(f"{constraint[1]}y = {constraint[2]}")
                st.latex(f"y = {float(y_intercept[0]):g}")
                st.write(f"  Perpotongan dengan sumbu y: y = {float(y_intercept[0]):g}")
        else:
            y_intercept = [None]  # Jika x=0, tidak ada intercept dengan y
        
        # Menyimpan batasan untuk plot grafik jika tidak ada hasil 0
        if x_intercept[0] is not None and y_intercept[0] is not None:
            solutions.append((float(x_intercept[0]), float(y_intercept[0])))
    
    return solutions


# Fungsi untuk membuat plot grafik batasan dan daerah feasible
# Fungsi untuk membuat plot grafik batasan dan daerah feasible
def plot_lp(solutions, constraints):
    x_vals = np.linspace(0, 10, 400)
    plt.figure(figsize=(8, 8))

    for i, constraint in enumerate(constraints):
        a, b, c = constraint
        if a != 0 and b != 0:  # Pastikan a dan b bukan 0
            y_vals = (c - a * x_vals) / b
            plt.plot(x_vals, y_vals, label=f'Batasan {i+1}')
        
            # Garis putus-putus (untuk memperjelas daerah feasible)
            plt.fill_between(x_vals, y_vals, where=(y_vals >= 0), alpha=0.2)
    
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
        solutions = calculate_lp(z, constraints)
        plot_lp(solutions, constraints)

if __name__ == "__main__":
    main()
