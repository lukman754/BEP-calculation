import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk membuat plot grafik batasan dan daerah feasible
def plot_lp(solutions, constraints, max_x, max_y):
    # Buat skala sumbu dinamis berdasarkan nilai maksimum
    x_vals = np.linspace(0, max(max_x, 10), 400)
    plt.figure(figsize=(8, 8))

    for i, constraint in enumerate(constraints):
        a, b, c = constraint

        # Jika b != 0, maka hitung y_vals
        if b != 0:
            y_vals = (c - a * x_vals) / b
            # Filter nilai tak hingga atau NaN dengan np.isfinite
            y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
            plt.plot(x_vals, y_vals, label=f'Batasan {i+1}')
            # Plot daerah feasible hanya jika y_vals valid
            plt.fill_between(x_vals, y_vals, where=~np.isnan(y_vals) & (y_vals >= 0), alpha=0.2)
        else:
            # Jika b == 0, garis vertikal x = c / a
            if a != 0:
                x_vert = c / a
                if 0 <= x_vert <= max(max_x, 10):
                    plt.axvline(x=x_vert, linestyle='--', label=f'Batasan {i+1} (garis vertikal)')
    
    # Set batas skala sumbu sesuai nilai maksimum
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
    # Dapatkan input fungsi tujuan dan batasan dari pengguna
    z, constraints = get_input()
    
    if st.button("Hitung dan Tampilkan Grafik"):
        solutions, max_x, max_y = calculate_lp(z, constraints)
        plot_lp(solutions, constraints, max_x, max_y)

if __name__ == "__main__":
    main()
