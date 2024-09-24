import streamlit as st
import matplotlib.pyplot as plt

def format_rupiah(value):
    """Format the value to Rupiah currency format."""
    return f"Rp {value:,.2f}"

def parse_rupiah(value):
    """Parse the formatted Rupiah string back to a float."""
    return float(value.replace("Rp ", "").replace(",", "").strip())

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
    units = list(range(units_sold + 1))
    total_revenue = [price_per_unit * unit for unit in units]  # TR
    total_variable_cost = [variable_cost_per_unit * unit for unit in units]  # TVC
    total_cost = [fixed_cost + total_variable_cost[i] for i in range(units_sold + 1)]  # TC
    profit_or_loss = [total_revenue[i] - total_cost[i] for i in range(units_sold + 1)]  # TR - TC

    plt.figure(figsize=(12, 8))
    
    # Grafik Total Pendapatan
    plt.plot(units, total_revenue, label="Total Pendapatan (TR)", color="green", linestyle='-', marker='o')
    
    # Grafik Total Biaya
    plt.plot(units, total_cost, label="Total Biaya (TC)", color="red", linestyle='-', marker='x')
    
    # Grafik Keuntungan/Kerugian
    plt.plot(units, profit_or_loss, label="Keuntungan/Kerugian (TR - TC)", color="blue", linestyle='-', marker='s')
    
    plt.axhline(0, color='black', linestyle='--')  # Garis impas (BEP)

    plt.title("Grafik Keuntungan atau Kerugian Berdasarkan Unit Terjual", fontsize=16)
    plt.xlabel("Jumlah Unit", fontsize=14)
    plt.ylabel("Rupiah", fontsize=14)
    plt.legend(fontsize=12)
    
    # Grid and markers
    plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    st.pyplot(plt)

def input_form():
    st.title("Kalkulator Keuntungan atau Kerugian dan Target Keuntungan")

    # Input dari pengguna
    fixed_cost = st.text_input("Masukkan Biaya Tetap (FC) (Rp)", value=format_rupiah(0), key='fixed_cost')
    price_per_unit = st.text_input("Masukkan Harga Jual per Unit (P) (Rp)", value=format_rupiah(0), key='price_per_unit')
    variable_cost_per_unit = st.text_input("Masukkan Biaya Variabel per Unit (AVC) (Rp)", value=format_rupiah(0), key='variable_cost_per_unit')
    units_sold = st.number_input("Masukkan Jumlah Unit Terjual (Q)", min_value=0, step=1)
    target_profit = st.text_input("Masukkan Target Keuntungan (Rp)", value=format_rupiah(0), key='target_profit')

    if st.button('Hitung'):
        # Parse the formatted Rupiah inputs back to float
        fixed_cost = parse_rupiah(fixed_cost)
        price_per_unit = parse_rupiah(price_per_unit)
        variable_cost_per_unit = parse_rupiah(variable_cost_per_unit)
        target_profit = parse_rupiah(target_profit)

        # Hitung keuntungan/kerugian
        total_revenue, total_cost, profit_or_loss = calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

        # Hitung jumlah unit yang diperlukan untuk mencapai target keuntungan
        required_units_for_target = calculate_units_for_target_profit(fixed_cost, price_per_unit, variable_cost_per_unit, target_profit)

        # Tampilkan hasil detail
        st.subheader("=== Hasil Detail ===")
        st.write(f"**Rumus Total Pendapatan (TR):** TR = P . Q")
        st.write(f"TR = {price_per_unit} x {units_sold}")
        st.write(f"**Total Pendapatan:** {format_rupiah(total_revenue)}")

        st.write(f"**Rumus Total Biaya (TC):** TC = FC + TVC = FC + AVC . Q")
        st.write(f"TC = {fixed_cost} + ({variable_cost_per_unit} x {units_sold})")
        st.write(f"**Total Biaya:** {format_rupiah(total_cost)}")

        if profit_or_loss > 0:
            st.success(f"**Keuntungan (TR > TC):** {format_rupiah(profit_or_loss)}")
        elif profit_or_loss < 0:
            st.error(f"**Kerugian (TR < TC):** {format_rupiah(-profit_or_loss)}")
        else:
            st.info("**Break Even Point (TR = TC):** Tidak ada keuntungan atau kerugian.")

        st.write(f"**Rumus BEP (unit):** BEP(unit) = FC / (P - AVC)")
        st.write(f"BEP(unit) = {fixed_cost} / ({price_per_unit} - {variable_cost_per_unit})")
        
        st.write(f"**Rumus BEP (Rp):** BEP(Rp.) = FC / (1 - AVC / P)")
        st.write(f"BEP(Rp.) = {fixed_cost} / (1 - {variable_cost_per_unit}/{price_per_unit})")

        st.write(f"**Untuk mencapai target keuntungan {format_rupiah(target_profit)}, Anda perlu menjual {required_units_for_target:.2f} unit.**")

        # Tampilkan grafik keuntungan/kerugian
        plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

# Jalankan form Streamlit
input_form()
