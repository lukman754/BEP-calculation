import matplotlib.pyplot as plt

def calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    # Menghitung total pendapatan, total biaya, dan keuntungan/kerugian
    total_revenue = price_per_unit * units_sold
    total_variable_cost = variable_cost_per_unit * units_sold
    total_cost = fixed_cost + total_variable_cost
    profit_or_loss = total_revenue - total_cost

    return total_revenue, total_cost, profit_or_loss

def calculate_units_for_target_profit(fixed_cost, price_per_unit, variable_cost_per_unit, target_profit):
    # Menghitung jumlah unit yang perlu dijual untuk mencapai target keuntungan
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
    plt.show()

def input_form():
    print("Form Dinamis untuk Menghitung Keuntungan atau Kerugian dan Target Keuntungan")

    # Input dari pengguna
    fixed_cost = float(input("Masukkan Biaya Tetap (Rp): "))
    price_per_unit = float(input("Masukkan Harga Jual per Unit (Rp): "))
    variable_cost_per_unit = float(input("Masukkan Biaya Variabel per Unit (Rp): "))
    units_sold = int(input("Masukkan Jumlah Unit Terjual: "))
    target_profit = float(input("Masukkan Target Keuntungan (Rp): "))

    # Hitung keuntungan/kerugian
    total_revenue, total_cost, profit_or_loss = calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

    # Hitung jumlah unit yang diperlukan untuk mencapai target keuntungan
    required_units_for_target = calculate_units_for_target_profit(fixed_cost, price_per_unit, variable_cost_per_unit, target_profit)

    # Tampilkan hasil detail
    print("\n=== Hasil Detail ===")
    print(f"Rumus Keuntungan: Total Pendapatan - Total Biaya")
    print(f"Total Pendapatan: Rp {total_revenue:,.2f} (Harga per Unit x Jumlah Unit Terjual)")
    print(f"Total Biaya: Rp {total_cost:,.2f} (Biaya Tetap + (Biaya Variabel per Unit x Jumlah Unit Terjual))")

    if profit_or_loss > 0:
        print(f"Keuntungan: Rp {profit_or_loss:,.2f}")
    elif profit_or_loss < 0:
        print(f"Kerugian: Rp {-profit_or_loss:,.2f}")
    else:
        print("Break Even Point, tidak ada keuntungan atau kerugian.")

    print(f"Rumus Target Keuntungan: (Biaya Tetap + Target Keuntungan) / (Harga per Unit - Biaya Variabel per Unit)")
    print(f"Untuk mencapai target keuntungan Rp {target_profit:,.2f}, Anda perlu menjual {required_units_for_target:.2f} unit.")
    
    # Tampilkan grafik keuntungan/kerugian
    plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

# Jalankan program
input_form()
