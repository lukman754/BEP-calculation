import streamlit as st
import numpy as np

# Fungsi untuk metode Sudut Barat Laut
def northwest_corner(supply, demand):
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    solution = np.zeros((len(supply), len(demand)))
    
    i, j = 0, 0
    while i < len(supply) and j < len(demand):
        min_val = min(supply_copy[i], demand_copy[j])
        solution[i, j] = min_val
        supply_copy[i] -= min_val
        demand_copy[j] -= min_val
        if supply_copy[i] == 0:
            i += 1
        if demand_copy[j] == 0:
            j += 1
    return solution

# Fungsi untuk metode Biaya Terendah
def least_cost(supply, demand, cost):
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    solution = np.zeros((len(supply), len(demand)))
    
    while supply_copy.sum() > 0 and demand_copy.sum() > 0:
        min_cost_index = np.unravel_index(np.argmin(cost, axis=None), cost.shape)
        i, j = min_cost_index
        min_val = min(supply_copy[i], demand_copy[j])
        solution[i, j] = min_val
        supply_copy[i] -= min_val
        demand_copy[j] -= min_val
        cost[i, j] = np.inf  # Set biaya jadi tak terhingga setelah dialokasikan
    return solution

# Fungsi untuk metode VAM
def vogel_approximation(supply, demand, cost):
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    solution = np.zeros((len(supply), len(demand)))

    while supply_copy.sum() > 0 and demand_copy.sum() > 0:
        row_penalty = np.apply_along_axis(lambda row: sorted(row)[1] - sorted(row)[0] if len(row) > 1 else 0, 1, cost)
        col_penalty = np.apply_along_axis(lambda col: sorted(col)[1] - sorted(col)[0] if len(col) > 1 else 0, 0, cost)

        max_row_penalty = np.max(row_penalty)
        max_col_penalty = np.max(col_penalty)

        if max_row_penalty > max_col_penalty:
            row = np.argmax(row_penalty)
            col = np.argmin(cost[row, :])
        else:
            col = np.argmax(col_penalty)
            row = np.argmin(cost[:, col])

        min_val = min(supply_copy[row], demand_copy[col])
        solution[row, col] = min_val
        supply_copy[row] -= min_val
        demand_copy[col] -= min_val
        cost[row, col] = np.inf

    return solution

# Streamlit UI
st.title("Metode Transportasi: Northwest, Least Cost, dan VAM")

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

# Convert ke numpy array
cost_matrix = np.array(cost_matrix)
supply = np.array(supply)
demand = np.array(demand)

# Pilihan metode
method = st.selectbox("Pilih Metode", ["Sudut Barat Laut", "Biaya Terendah", "VAM"])

# Tombol untuk menyelesaikan masalah
if st.button("Selesaikan"):
    if supply.sum() != demand.sum():
        st.error("Total suplai harus sama dengan total permintaan!")
    else:
        if method == "Sudut Barat Laut":
            solution = northwest_corner(supply, demand)
        elif method == "Biaya Terendah":
            solution = least_cost(supply, demand, cost_matrix.copy())
        else:  # VAM
            solution = vogel_approximation(supply, demand, cost_matrix.copy())

        st.success(f"Solusi dengan metode {method}:")
        st.write(solution)
