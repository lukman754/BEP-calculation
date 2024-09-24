def input_form():
    st.title("Kalkulator Keuntungan atau Kerugian dan Target Keuntungan", anchor=' Kalkulator')

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

        # Hitung titik impas
        break_even_units = calculate_break_even_point(fixed_cost, price_per_unit, variable_cost_per_unit)
        break_even_revenue = calculate_break_even_revenue(fixed_cost, price_per_unit, variable_cost_per_unit)

        # Tampilkan hasil detail
        st.subheader("=== Hasil Detail ===")
        
        # Display formulas separately
        st.write("**Rumus Total Pendapatan (TR):**")
        st.write(f"TR = P . Q")
        st.write(f"TR = {price_per_unit} x {units_sold} = Rp {total_revenue:,.2f}")
        
        st.write("**Rumus Total Biaya (TC):**")
        st.write(f"TC = FC + TVC = FC + AVC . Q")
        st.write(f"TC = {fixed_cost} + ({variable_cost_per_unit} x {units_sold}) = Rp {total_cost:,.2f}")

        # Result message for profit/loss
        if profit_or_loss > 0:
            st.success(f"**Keuntungan (TR > TC):** Rp {profit_or_loss:,.2f}")
        elif profit_or_loss < 0:
            st.error(f"**Kerugian (TR < TC):** Rp {-profit_or_loss:,.2f}")
        else:
            st.info("**Break Even Point (TR = TC):** Tidak ada keuntungan atau kerugian.")

        # Display BEP results
        if break_even_units is not None:
            st.write("**Rumus BEP (unit):**")
            st.write(f"BEP(unit) = FC / (P - AVC)")
            st.write(f"BEP(unit) = {fixed_cost} / ({price_per_unit} - {variable_cost_per_unit}) = {break_even_units:.2f} unit")

            st.write("**Rumus BEP (Rp):**")
            st.write(f"BEP(Rp.) = FC / (1 - AVC / P)")
            st.write(f"BEP(Rp.) = {fixed_cost} / (1 - {variable_cost_per_unit}/{price_per_unit}) = Rp {break_even_revenue:,.2f}")

        # Display the formula for target profit
        st.write("**Rumus Unit yang Harus Dijual untuk Mencapai Target Keuntungan:**")
        st.write("Jumlah Unit = (FC + Target Keuntungan) / (P - AVC)")
        st.write(f"Jumlah Unit = ({fixed_cost} + {target_profit}) / ({price_per_unit} - {variable_cost_per_unit}) = {required_units_for_target:.2f} unit")

        # Display the required units for target profit
        st.write(f"**Untuk mencapai target keuntungan Rp {target_profit:,.2f}, Anda perlu menjual {required_units_for_target:.2f} unit.**")

        # Tampilkan grafik keuntungan/kerugian
        plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

# Jalankan form Streamlit
input_form()
