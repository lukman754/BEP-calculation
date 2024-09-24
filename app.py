import streamlit as st
import matplotlib.pyplot as plt

def calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    total_revenue = price_per_unit * units_sold
    total_variable_cost = variable_cost_per_unit * units_sold
    total_cost = fixed_cost + total_variable_cost
    profit_or_loss = total_revenue - total_cost

    return total_revenue, total_cost, profit_or_loss

def calculate_units_for_target_profit(fixed_cost, price_per_unit, variable_cost_per_unit, target_profit):
    required_units = (fixed_cost + target_profit) / (price_per_unit - variable_cost_per_unit)
    return required_units

def plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    units = list(range(units_sold + 1))
    total_revenue = [price_per_unit * unit for unit in units]
    total_variable_cost = [variable_cost_per_unit * unit for unit in units]
    total_cost = [fixed_cost + total_variable_cost[i] for i in range(units_sold + 1)]
    profit_or_loss = [total_revenue[i] - total_cost[i] for i in range(units_sold + 1)]

    plt.figure(figsize=(10, 6))
    plt.plot(units, total_revenue, label="Total Pendapatan", color="green")
    plt.plot(units, total_cost, label="Total Biaya", color="red")
    plt.plot(units, profit_or_loss, label="Keuntungan/Kerugian", color="blue")
    plt.axhline(0, color='black', linestyle='--')  # Garis impas (keuntungan = 0)
    plt.title("Grafik Keuntungan atau Kerugian Berdasarkan Unit Terjual")
    plt.xlabel("Jumlah Unit")
    plt.ylabel("Rupiah")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)  # Display the plot in Streamlit

def input_form():
    st.title("Kalkulator Keuntungan atau Kerugian dan Target Keuntungan")

    # Input dari pengguna
    fixed_cost = st.number_input("Masukkan Biaya Tetap (Rp)", min_value=0.0, step=100.0)
    price_per_unit = st.number_input("Masukkan Harga Jual per Unit (Rp)", min_value=0.0, step=100.0)
    variable_cost_per_unit = st.number_input("Masukkan Biaya Variabel per Unit (Rp)", min_value=0.0, step=100.0)
    units_sold = st.number_input("Masukkan Jumlah Unit Terjual", min_value=0, step=1)
    target_profit = st.number_input("Masukkan Target Keuntungan (Rp)", min_value=0.0, step=100.0)

    if st.button('Hitung'):
        # Hitung keuntungan/kerugian
        total_revenue, total_cost, profit_or_loss = calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

        # Hitung jumlah unit yang diperlukan untuk mencapai target keuntungan
        required_units_for_target = calculate_units_for_target_profit(fixed_cost, price_per_unit, variable_cost_per_unit, target_profit)

        # Tampilkan hasil detail
        st.subheader("=== Hasil Detail ===")
        st.write(f"Total Pendapatan: Rp {total_revenue:,.2f}")
        st.write(f"Total Biaya: Rp {total_cost:,.2f}")

        if profit_or_loss > 0:
            st.success(f"Keuntungan: Rp {profit_or_loss:,.2f}")
        elif profit_or_loss < 0:
            st.error(f"Kerugian: Rp {-profit_or_loss:,.2f}")
        else:
            st.info("Break Even Point, tidak ada keuntungan atau kerugian.")

        st.write(f"Untuk mencapai target keuntungan Rp {target_profit:,.2f}, Anda perlu menjual {required_units_for_target:.2f} unit.")

        # Tampilkan grafik keuntungan/kerugian
        plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

# Jalankan form Streamlit
input_form()
