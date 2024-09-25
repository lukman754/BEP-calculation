import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve

# Fungsi untuk menampilkan input dinamis dengan streamlit
def get_input():
    st.title("Kalkulator Linear Programming (Metode Grafik)")
    
    st.header("Input Fungsi Tujuan")
    z = [
        st.number_input("Koefisien x pada fungsi tujuan", value=1.0, key="z_x"),
        st.number_input("Koefisien y pada fungsi tujuan", value=1.0, key="z_y")
    ]
    
    num_constraints = st.number_input("Jumlah Batasan", min_value=1, max_value=5, step=1, value=2, key="num_constraints")
    st.header("Input Batasan")
    
    constraints = []
    for i in range(num_constraints):
        st.subheader(f"Batasan {i+1}")
        a = st.number_input(f"Koefisien x pada batasan {i+1}", value=1.0, key=f"a_{i}")
        b = st.number_input(f"Koefisien y pada batasan {i+1}", value=1.0, key=f"b_{i}")
        c = st.number_input(f"Nilai batasan {i+1} (<=)", value=1.0, key=f"c_{i}")
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
    
    # Proses setiap batasan
    for i, constraint in enumerate(constraints):
        st.subheader(f"Batasan {i+1}")
        st.write(f"Batasan: {constraint[0]}x + {constraint[1]}y <= {constraint[2]}")
        
        # Solusi perpotongan dengan sumbu x (y=0)
        x_intercept = constraint[2] / constraint[0] if constraint[0] != 0 else None
        if x_intercept is not None:
            st.write(f"  Perpotongan dengan sumbu x: x = {x_intercept:.2f}")
        
        # Solusi perpotongan dengan sumbu y (x=0)
        y_intercept = constraint[2] / constraint[1] if constraint[1] != 0 else None
        if y_intercept is not None:
            st.write(f"  Perpotongan dengan sumbu y: y = {y_intercept:.2f}")
        
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
    
    st.pyplot(plt)

# Main function for Streamlit app
def main():
    z, constraints = get_input()
    
    if st.button("Hitung dan Tampilkan Grafik"):
        solutions = calculate_lp(z, constraints)
        plot_lp(solutions, constraints)

if __name__ == "__main__":
    main()
