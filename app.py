import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk menghitung total pendapatan, total biaya, dan untung/rugi
def calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    total_revenue = price_per_unit * units_sold  # TR = P * Q
    total_variable_cost = variable_cost_per_unit * units_sold  # TVC = AVC * Q
    total_cost = fixed_cost + total_variable_cost  # TC = FC + TVC
    profit_or_loss = total_revenue - total_cost  # Profit or Loss = TR - TC
    return total_revenue, total_cost, profit_or_loss

# Fungsi untuk menghitung Break Even Point (BEP)
def calculate_break_even_units(fixed_cost, price_per_unit, variable_cost_per_unit):
    break_even_units = fixed_cost / (price_per_unit - variable_cost_per_unit)  # BEP(unit)
    return break_even_units

# Fungsi untuk menampilkan grafik pendapatan, biaya, dan BEP
def plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    units = list(range(units_sold + 1))
    total_revenue = [price_per_unit * unit for unit in units]  # TR = P * Q
    total_variable_cost = [variable_cost_per_unit * unit for unit in units]  # TVC = AVC * Q
    total_cost = [fixed_cost + total_variable_cost[i] for i in range(units_sold + 1)]  # TC = FC + TVC
    profit_or_loss = [total_revenue[i] - total_cost[i] for i in range(units_sold + 1)]  # TR - TC

    # Menghitung BEP dalam unit dan rupiah
    break_even_units = calculate_break_even_units(fixed_cost, price_per_unit, variable_cost_per_unit)
    break_even_revenue = price_per_unit * break_even_units  # BEP dalam Rupiah

    # Membuat grafik
    plt.figure(figsize=(10, 6))

    # Garis Total Pendapatan (TR)
    plt.plot(units, total_revenue, label="Total Pendapatan (TR)", color="green")

    # Garis Total Biaya (TC)
    plt.plot(units, total_cost, label="Total Biaya (TC)", color="red")

    # Garis Biaya Tetap (FC)
    plt.axhline(y=fixed_cost, color='purple', linestyle='--', label="Biaya Tetap (FC)")

    # Menandai Break Even Point
    plt.axvline(x=break_even_units, color='blue', linestyle='--', label=f"BEP (Unit: {break_even_units:.2f})")
    plt.axhline(y=break_even_revenue, color='blue', linestyle='--', label=f"BEP (Rp: {break_even_revenue:.2f})")

    # Area Rugi dan Untung
    plt.fill_between(units, total_revenue, total_cost, where=(total_revenue <= total_cost), color='orange', alpha=0.3, label="Daerah Rugi")
    plt.fill_between(units, total_revenue, total_cost, where=(total_revenue > total_cost), color='yellow', alpha=0.3, label="Daerah Untung")

    # Pengaturan tampilan grafik
    plt.title("Grafik Keuntungan atau Kerugian Berdasarkan Unit Terjual")
    plt.xlabel("Jumlah Unit (Q)")
    plt.ylabel("Rupiah (Rp)")
    plt.legend()

    # Tampilkan grafik di Streamlit
    st.pyplot(plt)

# Bagian utama Streamlit
st.title("Perhitungan Break Even Point (BEP), Untung, dan Rugi")

# Input pengguna
fixed_cost = st.number_input("Masukkan Biaya Tetap (FC) dalam Rupiah:", min_value=0, value=5000000, step=100000)
price_per_unit = st.number_input("Masukkan Harga Jual per Unit (P) dalam Rupiah:", min_value=0, value=5500, step=100)
variable_cost_per_unit = st.number_input("Masukkan Biaya Variabel per Unit (AVC) dalam Rupiah:", min_value=0, value=3500, step=100)
units_sold = st.number_input("Masukkan Jumlah Unit Terjual (Q):", min_value=1, value=2500, step=100)

# Perhitungan total pendapatan, total biaya, dan untung/rugi
total_revenue, total_cost, profit_or_loss = calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

# Hitung BEP
break_even_units = calculate_break_even_units(fixed_cost, price_per_unit, variable_cost_per_unit)

# Tampilkan hasil
st.subheader("Hasil Perhitungan:")
st.write(f"**Total Pendapatan (TR): Rp {total_revenue:,.2f}**")
st.write(f"**Total Biaya (TC): Rp {total_cost:,.2f}**")
st.write(f"**Keuntungan/Kerugian: Rp {profit_or_loss:,.2f}**")
st.write(f"**Break Even Point (BEP) dalam Unit: {break_even_units:.2f} Unit**")

# Tampilkan grafik
plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)
