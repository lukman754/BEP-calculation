import streamlit as st
import numpy as np
from scipy.optimize import linprog

# Fungsi untuk menyelesaikan masalah transportasi
def solve_transportation(supply, demand, cost_matrix):
    num_suppliers = len(supply)
    num_customers = len(demand)
    
    # Membuat koefisien objektif
    c = cost_matrix.flatten()  # Biaya per pengiriman
    
    # Membuat batasan (constraint)
    A_eq = []
    b_eq = []

    # Pembatasan untuk suplai
    for i in range(num_suppliers):
        constraint = [0] * num_suppliers * num_customers
        for j in range(num_customers):
            constraint[i * num_customers + j] = 1
        A_eq.append(constraint)
        b_eq.append(supply[i])

    # Pembatasan untuk permintaan
    for j in range(num_customers):
        constraint = [0] * num_suppliers * num_customers
        for i in range(num_suppliers):
            constraint[i * num_customers + j] = 1
        A_eq.append(constraint)
        b_eq.append(demand[j])

    A_eq = np.array(A_eq)
    b_eq = np.array(b_eq)

    # Batasan non-negatif
    bounds = [(0, None)] * (num_suppliers * num_customers)

    # Menyelesaikan masalah linier programming
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    return result

# Streamlit UI
st.title("Metode Transportasi - Linear Programming")

# Input jumlah supplier dan customer
num_suppliers = st.number_input("Jumlah Supplier", min_value=2, max_value=10, value=3, step=1)
num_customers = st.number_input("Jumlah Customer", min_value=2, max_value=10, value=3, step=1)

# Input kapasitas suplai
st.subheader("Kapasitas Suplai (Supply)")
supply = []
for i in range(num_suppliers):
    supply.append(st.number_input(f"Suplai dari Supplier {i+1}", min_value=0, step=1))

# Input permintaan demand
st.subheader("Permintaan (Demand)")
demand = []
for j in range(num_customers):
    demand.append(st.number_input(f"Permintaan dari Customer {j+1}", min_value=0, step=1))

# Input matriks biaya transportasi
st.subheader("Biaya Transportasi")
cost_matrix = []
for i in range(num_suppliers):
    row = []
    for j in range(num_customers):
        row.append(st.number_input(f"Biaya Supplier {i+1} ke Customer {j+1}", min_value=0, step=1))
    cost_matrix.append(row)

# Tombol untuk menyelesaikan masalah
if st.button("Selesaikan"):
    supply = np.array(supply)
    demand = np.array(demand)
    cost_matrix = np.array(cost_matrix)

    if supply.sum() != demand.sum():
        st.error("Total suplai harus sama dengan total permintaan!")
    else:
        result = solve_transportation(supply, demand, cost_matrix)
        if result.success:
            st.success("Masalah terselesaikan!")
            st.write("Solusi Optimasi (Jumlah Pengiriman):")
            solution_matrix = result.x.reshape((num_suppliers, num_customers))
            st.write(solution_matrix)
        else:
            st.error("Tidak ditemukan solusi yang sesuai!")
