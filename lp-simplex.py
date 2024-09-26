import streamlit as st
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpStatus, value

# Fungsi untuk menghitung solusi linear programming
def solve_linear_programming(objective_coeffs, constraints, rhs, constraint_inequalities):
    # Buat model LP
    model = LpProblem("Linear_Programming_Problem", LpMaximize)

    # Buat variabel
    vars = [LpVariable(f'x{i}', lowBound=0) for i in range(len(objective_coeffs))]

    # Tambahkan fungsi objektif
    model += lpSum([objective_coeffs[i] * vars[i] for i in range(len(objective_coeffs))])

    # Tambahkan constraint
    for i in range(len(constraints)):
        if constraint_inequalities[i] == "<=":
            model += lpSum([constraints[i][j] * vars[j] for j in range(len(vars))]) <= rhs[i]
        elif constraint_inequalities[i] == ">=":
            model += lpSum([constraints[i][j] * vars[j] for j in range(len(vars))]) >= rhs[i]

    # Selesaikan model
    model.solve()

    # Kembalikan status dan nilai
    return LpStatus[model.status], [value(var) for var in vars], value(model.objective)

# UI Streamlit
st.title("Kalkulator Linear Programming - Metode Simpleks")

# Input untuk koefisien fungsi objektif
st.header("Fungsi Objektif")
num_objectives = st.number_input("Jumlah Variabel pada Fungsi Objektif", min_value=1, value=2)
objective_coeffs = st.text_input("Koefisien Fungsi Objektif (pisahkan dengan koma)", "2, 3").split(",")

# Input untuk constraint
st.header("Constraints")
num_constraints = st.number_input("Jumlah Constraint", min_value=1, value=1)
constraints = []
rhs = []
inequalities = []

for i in range(num_constraints):
    st.subheader(f"Constraint {i + 1}")
    constraint_coeffs = st.text_input(f"Koefisien Constraint {i + 1} (pisahkan dengan koma)", "1, 1").split(",")
    constraints.append(list(map(float, constraint_coeffs)))
    rhs_value = st.number_input(f"Nilai RHS untuk Constraint {i + 1}", value=10)
    rhs.append(rhs_value)
    inequality = st.selectbox(f"Inequality untuk Constraint {i + 1}", ["<=", ">="], key=f"ineq_{i}")
    inequalities.append(inequality)

# Tombol untuk menghitung
if st.button("Hitung"):
    # Mengkonversi input menjadi tipe yang sesuai
    objective_coeffs = list(map(float, objective_coeffs))
    status, solution, objective_value = solve_linear_programming(objective_coeffs, constraints, rhs, inequalities)

    # Menampilkan hasil
    st.write("Status Solusi:", status)
    st.write("Solusi Optimal:", solution)
    st.write("Nilai Fungsi Objektif Maksimum:", objective_value)
