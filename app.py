import streamlit as st
import matplotlib.pyplot as plt

def calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    total_revenue = price_per_unit * units_sold  # TR = P . Q
    total_variable_cost = variable_cost_per_unit * units_sold  # TVC = AVC . Q
    total_cost = fixed_cost + total_variable_cost  # TC = FC + TVC
    profit_or_loss = total_revenue - total_cost  # TR - TC

    return total_revenue, total_cost, profit_or_loss

def calculate_units_for_target_profit(fixed_cost, price_per_unit, variable_cost_per_unit, target_profit):
    required_units = (fixed_cost + target_profit) / (price_per_unit - variable_cost_per_unit)  # BEP(unit)
    return required_units

def plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    if price_per_unit <= variable_cost_per_unit:
        st.error("Harga Jual per Unit harus lebih besar dari Biaya Variabel per Unit untuk menghitung BEP.")
        return

    units = list(range(units_sold + 1))
    total_revenue = [price_per_unit * unit for unit in units]  # TR
    total_variable_cost = [variable_cost_per_unit * unit for unit in units]  # TVC
    total_cost = [fixed_cost + total_variable_cost[i] for i in range(len(units))]  # TC
    break_even_units = fixed_cost / (price_per_unit - variable_cost_per_unit) if (price_per_unit - variable_cost_per_unit) > 0 else 0  # BEP (units)

    # Adjust the plot for the graphic
    plt.figure(figsize=(12, 8))

    # Grafik Total Pendapatan (TR)
    plt.plot(units, total_revenue, label="Total Pendapatan (TR)", color="green", linestyle='-', marker='o')

    # Grafik Total Biaya (TC)
    plt.plot(units, total_cost, label="Total Biaya (TC)", color="red", linestyle='-', marker='x')

    # Break-even point (BEP)
    if break_even_units > 0:
        plt.axvline(break_even_units, color="black", linestyle="--", label=f"BEP = {break_even_units:.2f} units")

    # Add shading for Daerah Rugi and Daerah Untung
    plt.fill_between(units, total_cost, total_revenue, where=(total_revenue < total_cost), color='gray', alpha=0.5, label='Daerah Rugi')
    plt.fill_between(units, total_cost, total_revenue, where=(total_revenue > total_cost), color='green', alpha=0.5, label='Daerah Untung')

    # Title and labels
    plt.title("Grafik Keuntungan atau Kerugian Berdasarkan Unit Terjual", fontsize=16)
    plt.xlabel("Jumlah Unit (Q)", fontsize=14)
    plt.ylabel("Rupiah (Rp.)", fontsize=14)
    plt.legend(fontsize=12)

    # Grid and markers
    plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    st.pyplot(plt)


def input_form():
    st.title("Kalkulator Keuntungan atau Kerugian dan Target Keuntungan")

    # Input dari pengguna
    fixed_cost = st.number_input("Masukkan Biaya Tetap (FC) (Rp)", min_value=0.0, step=100.0)
    price_per_unit = st.number_input("Masukkan Harga Jual per Unit (P) (Rp)", min_value=0.0, step=100.0)
    variable_cost_per_unit = st.number_input("Masukkan Biaya Variabel per Unit (AVC) (Rp)", min_value=0.0, step=100.0)
    units_sold = st.number_input("Masukkan Jumlah Unit Terjual (Q)", min_value=0, step=1)
    target_profit = st.number_input("Masukkan Target Keuntungan (Rp)", min_value=0.0, step=100.0)

    if st.button('Hitung'):
        # Hitung keuntungan/kerugian
        total_revenue, total_cost, profit_or_loss = calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

        # Hitung jumlah unit yang diperlukan untuk mencapai target keuntungan
        required_units_for_target = calculate_units_for_target_profit(fixed_cost, price_per_unit, variable_cost_per_unit, target_profit)

        # Tampilkan hasil detail
        st.subheader("=== Hasil Detail ===")
        st.write(f"**Rumus Total Pendapatan (TR):** TR = P . Q")
        st.write(f"TR = {price_per_unit} x {units_sold}")
        st.write(f"**Total Pendapatan:** Rp {total_revenue:,.2f}")

        st.write(f"**Rumus Total Biaya (TC):** TC = FC + TVC = FC + AVC . Q")
        st.write(f"TC = {fixed_cost} + ({variable_cost_per_unit} x {units_sold})")
        st.write(f"**Total Biaya:** Rp {total_cost:,.2f}")

        if profit_or_loss > 0:
            st.success(f"**Keuntungan (TR > TC):** Rp {profit_or_loss:,.2f}")
        elif profit_or_loss < 0:
            st.error(f"**Kerugian (TR < TC):** Rp {-profit_or_loss:,.2f}")
        else:
            st.info("**Break Even Point (TR = TC):** Tidak ada keuntungan atau kerugian.")

        st.write(f"**Rumus BEP (unit):** BEP(unit) = FC / (P - AVC)")
        st.write(f"BEP(unit) = {fixed_cost} / ({price_per_unit} - {variable_cost_per_unit})")
        
        st.write(f"**Rumus BEP (Rp):** BEP(Rp.) = FC / (1 - AVC / P)")
        st.write(f"BEP(Rp.) = {fixed_cost} / (1 - {variable_cost_per_unit}/{price_per_unit})")

        st.write(f"**Untuk mencapai target keuntungan Rp {target_profit:,.2f}, Anda perlu menjual {required_units_for_target:.2f} unit.**")

        # Panggil fungsi untuk menampilkan grafik
        plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

# Jalankan form Streamlit
input_form()
