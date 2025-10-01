import os
import pandas as pd
import matplotlib.pyplot as plt


def run_job(input_directory, output_directory, plots_directory):
    """Genera summary.csv y top10_drivers.png"""

    # Crear carpetas de salida si no existen
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(plots_directory, exist_ok=True)

    # Cargar datasets
    drivers = pd.read_csv(os.path.join(input_directory, "drivers.csv"))
    timesheet = pd.read_csv(os.path.join(input_directory, "timesheet.csv"))

    # Unir por driverId
    merged = pd.merge(timesheet, drivers, on="driverId")

    # Resumen: total de horas y millas por conductor
    summary = merged.groupby(["driverId", "name"], as_index=False).agg({
        "hours-logged": "sum",
        "miles-logged": "sum"
    })

    # Guardar resumen
    summary_file = os.path.join(output_directory, "summary.csv")
    summary.to_csv(summary_file, index=False)

    # Top 10 conductores por millas
    top10 = summary.sort_values(by="miles-logged", ascending=False).head(10)

    # Gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(top10["name"], top10["miles-logged"])
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Driver")
    plt.ylabel("Miles Logged")
    plt.title("Top 10 Drivers by Miles")
    plt.tight_layout()

    # Guardar gráfico
    plot_file = os.path.join(plots_directory, "top10_drivers.png")
    plt.savefig(plot_file)
    plt.close()


if __name__ == "__main__":
    run_job(
        "files/input",
        "files/output",
        "files/plots"
    )
