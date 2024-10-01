import streamlit as st
import numpy as np

st.title('Kalkulator Linear Programming - Metode Substitusi')

# Input jumlah variabel dan jumlah persamaan
num_vars = st.number_input('Jumlah variabel', min_value=2, value=2)
num_eqs = st.number_input('Jumlah persamaan', min_value=2, value=2)

# Form untuk input koefisien persamaan
st.subheader("Masukkan koefisien dan konstanta persamaan:")
coefficients = []
for i in range(num_eqs):
    eq = []
    for j in range(num_vars):
        coeff = st.number_input(f'Koefisien x{j + 1} untuk Persamaan {i + 1}', key=f'coeff_{i}_{j}')
        eq.append(coeff)
    const = st.number_input(f'Konstanta untuk Persamaan {i + 1}', key=f'const_{i}')
    eq.append(const)
    coefficients.append(eq)

# Tampilkan persamaan yang dimasukkan
st.subheader("Persamaan yang dimasukkan:")
for i, eq in enumerate(coefficients):
    equation = " + ".join([f"{coeff}x{j + 1}" for j, coeff in enumerate(eq[:-1])])
    equation += f" = {eq[-1]}"
    st.write(f"Persamaan {i + 1}: {equation}")

# Fungsi untuk menyelesaikan dengan metode substitusi
def substitution_method(coefficients):
    a1, b1, c1 = coefficients[0][0], coefficients[0][1], coefficients[0][2]
    a2, b2, c2 = coefficients[1][0], coefficients[1][1], coefficients[1][2]
    
    # Hitung substitusi
    y = (c2 - a2 * (c1 / a1)) / (b2 - a2 * (b1 / a1))
    x = (c1 - b1 * y) / a1
    
    return x, y

# Kalkulasi solusi jika ada 2 persamaan dan 2 variabel
if num_eqs == 2 and num_vars == 2:
    if st.button('Hitung'):
        try:
            x, y = substitution_method(coefficients)
            st.success(f'Solusi: x = {x}, y = {y}')
        except ZeroDivisionError:
            st.error("Tidak dapat menyelesaikan, terjadi pembagian dengan nol.")
else:
    st.info("Saat ini metode substitusi hanya bisa digunakan untuk 2 persamaan dengan 2 variabel.")
