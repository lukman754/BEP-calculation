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
def calculate_lp(z, constraints):
    x, y = symbols('x y')
    
    # Tampilkan fungsi tujuan
    st.subheader("Fungsi Tujuan")
    st.write(f"Fungsi tujuan: {z[0]:g}x + {z[1]:g}y")
    
    # Menyimpan solusi batasan
    solutions = []
    
    # Proses setiap batasan
    for i, constraint in enumerate(constraints):
        st.subheader(f"Batasan {i+1}")
        st.write(f"Batasan: {constraint[0]:g}x + {constraint[1]:g}y <= {constraint[2]:g}")
        
        # Menggunakan persamaan untuk eliminasi atau substitusi
        equation = Eq(constraint[0]*x + constraint[1]*y, constraint[2])
        st.write(f"Persamaan batasan: {constraint[0]:g}x + {constraint[1]:g}y = {constraint[2]:g}")
        
        # Hanya hitung perpotongan jika koefisien tidak 0
        x_intercept = None
        y_intercept = None

        # Hitung jika salah satu koefisien tidak nol
        if constraint[0] != 0 and constraint[1] != 0:
            y_intercept = solve(equation.subs(x, 0), y)
            x_intercept = solve(equation.subs(y, 0), x)
            st.write(f"  Perpotongan dengan sumbu y: y = {float(y_intercept[0]):g}")
            st.write(f"  Perpotongan dengan sumbu x: x = {float(x_intercept[0]):g}")
            solutions.append((x_intercept[0], y_intercept[0]))

        elif constraint[0] != 0:  # Hanya x yang tidak nol
            x_intercept = solve(equation.subs(y, 0), x)
            st.write(f"  Perpotongan dengan sumbu x: x = {float(x_intercept[0]):g}")
            solutions.append((x_intercept[0], 0))  # y = 0

        elif constraint[1] != 0:  # Hanya y yang tidak nol
            y_intercept = solve(equation.subs(x, 0), y)
            st.write(f"  Perpotongan dengan sumbu y: y = {float(y_intercept[0]):g}")
            solutions.append((0, y_intercept[0]))  # x = 0

    return solutions

# Fungsi untuk membuat plot grafik batasan dan daerah feasible
def plot_lp(solutions, constraints):
    x_vals = np.linspace(0, 200, 400)  # Range x diperkecil untuk menyesuaikan tampilan
    plt.figure(figsize=(8, 8))

    x_max, y_max = 0, 0  # Inisialisasi batas maksimum untuk sumbu

    for i, constraint in enumerate(constraints):
        a, b, c = constraint
        
        # Hanya plot jika koefisien y bukan 0
        if b != 0:
            y_vals = (c - a * x_vals) / b
            linestyle = 'solid' if a != 0 else 'dashed'  # Solid jika kedua koefisien tidak nol, dashed jika hanya y
            plt.plot(x_vals, y_vals, label=f'Batasan {i+1}', linestyle=linestyle)
            plt.fill_between(x_vals, y_vals, where=(y_vals >= 0), alpha=0.2)

        # Jika hanya x yang tidak nol
        if a != 0 and b == 0:
            plt.axvline(x=c/a, linestyle='dashed', label=f'Batasan {i+1} (x hanya)', color='red')
        
        # Jika hanya y yang tidak nol
        if a == 0 and b != 0:
            plt.axhline(y=c/b, linestyle='dashed', label=f'Batasan {i+1} (y hanya)', color='blue')

        # Menyesuaikan batas sumbu berdasarkan nilai terbesar dari x dan y
        if a != 0:
            x_max = max(x_max, c / a)
        if b != 0:
            y_max = max(y_max, c / b)

    # Menghitung dan menampilkan titik perpotongan
    intersection_points = []
    for i in range(len(constraints)):
        for j in range(i + 1, len(constraints)):
            a1, b1, c1 = constraints[i]
            a2, b2, c2 = constraints[j]

            # Menghindari kasus di mana kedua koefisien adalah 0
            if a1 * b2 != a2 * b1:  # Jika garis tidak sejajar
                # Menghitung titik perpotongan
                x_val = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
                y_val = (c1 - a1 * x_val) / b1
                intersection_points.append((x_val, y_val))

    # Plot titik perpotongan
    for (x_val, y_val) in intersection_points:
        plt.plot(x_val, y_val, 'ro')  # Titik perpotongan berwarna merah
        plt.axvline(x=x_val, linestyle='dashed', color='grey', alpha=0.5)  # Garis vertikal putus-putus
        plt.axhline(y=y_val, linestyle='dashed', color='grey', alpha=0.5)  # Garis horizontal putus-putus
        plt.annotate(f'({x_val:.2f}, {y_val:.2f})', (x_val, y_val), textcoords="offset points", xytext=(0,10), ha='center')

    # Sesuaikan sumbu berdasarkan nilai maksimum
    plt.xlim(0, min(200, x_max * 1.1))  # Tambah 10% dari nilai max untuk ruang ekstra, batas 50 untuk skala lebih baik
    plt.ylim(0, min(200, y_max * 1.1))
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, which='both')

    plt.legend()
    plt.title("Grafik Linear Programming")
    plt.xlabel("x")
    plt.ylabel("y")
    
    st.pyplot(plt)

# Main function to run the app
def main():
    z, constraints = get_input()
    solutions = calculate_lp(z, constraints)
    plot_lp(solutions, constraints)

def add_footer():
    footer = """
    <style>
        .footer {
            width: 100%;
            text-align: center;
            padding: 10px;
            margin-top: 20px;
        }
    </style>
    <div class="footer">
        <p><b>Chopin</b> © 2024</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    add_footer()
