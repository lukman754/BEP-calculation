from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Fungsi untuk menghitung keuntungan/kerugian
def calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold):
    total_revenue = price_per_unit * units_sold
    total_variable_cost = variable_cost_per_unit * units_sold
    total_cost = fixed_cost + total_variable_cost
    profit_or_loss = total_revenue - total_cost
    return total_revenue, total_cost, profit_or_loss

# Fungsi untuk menggambar grafik BEP
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
    plt.axhline(0, color='black', linestyle='--')
    plt.xlabel("Jumlah Unit")
    plt.ylabel("Rupiah")
    plt.title("Grafik Keuntungan atau Kerugian")
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        fixed_cost = float(request.form.get("fixed_cost"))
        price_per_unit = float(request.form.get("price_per_unit"))
        variable_cost_per_unit = float(request.form.get("variable_cost_per_unit"))
        units_sold = int(request.form.get("units_sold"))

        total_revenue, total_cost, profit_or_loss = calculate_profit_or_loss(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)
        plot_url = plot_profit(fixed_cost, price_per_unit, variable_cost_per_unit, units_sold)

        return render_template("index.html", plot_url=plot_url, total_revenue=total_revenue, total_cost=total_cost, profit_or_loss=profit_or_loss)

    return render_template("index.html", plot_url=None)

if __name__ == "__main__":
    app.run(debug=True)
