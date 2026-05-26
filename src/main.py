import csv
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

from tkinter.filedialog import askopenfilename


def init_country_dict(_name, _year, _data1) -> dict:
    return dict(name=_name, year=_year, data1=_data1, data2=None)


def fill_data_set(paths: list, year: str, country_data: dict) -> None:
    for path in paths:
        with open(path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Year"] == year:
                    vlist = list(row.values())
                    code = vlist[1]

                    if code in country_data:
                        country_data[code]["data2"] = vlist[3]
                    else:
                        country_data[code] = init_country_dict(
                            vlist[1], vlist[2], vlist[3]
                        )


def purge_unmatched_pairs(country_data: dict) -> None:
    to_pop = []

    for code in country_data:
        if country_data[code]["data2"] == None:
            to_pop.append(code)

    for code in to_pop:
        country_data.pop(code)


def build_x_y(country_data: dict) -> tuple[list[float], list[float]]:
    countries_x = []
    countries_y = []

    for code in country_data:
        data = country_data[code]
        try:
            x = float(data["data1"])
            y = float(data["data2"])
        except (ValueError, TypeError):
            print(
                f"Skipping {code}: non-numeric value ({data['data1']!r}, {data['data2']!r})"
            )
            continue

        countries_x.append(x)
        countries_y.append(y)

    return countries_x, countries_y


def graph_and_calc_stats(
    countries_x: list[float],
    countries_y: list[float],
    title: str,
    x_title: str,
    y_title: str,
) -> dict:

    slope, intercept, r, p, std_err = linregress(countries_x, countries_y)
    r_squared = r**2

    plt.scatter(countries_x, countries_y)
    plt.plot(countries_x, slope * np.array(countries_x) + intercept)

    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)

    output_path = "statscsv/output/graph.png"
    plt.savefig(output_path)
    plt.close()

    return dict(
        slope=slope, intercept=intercept, r=r, p=p, std_err=std_err, r2=r_squared
    )


def main():
    year = input("Target Year: ")

    explanatory_path = askopenfilename(title="Select explanatory variable CSV")
    response_path = askopenfilename(title="Select response variable CSV")

    if not explanatory_path or not response_path:
        print("File selection cancelled.")
        return

    country_data = {}

    try:
        fill_data_set([explanatory_path, response_path], year, country_data)
    except Exception as e:
        print("Error occured: ", e)
        return

    purge_unmatched_pairs(country_data)

    if not country_data:
        print("No matched pairs found in given year.")
        return

    countries_x, countries_y = build_x_y(country_data)

    if len(countries_x) < 2:
        print("Not enough valid data points to run regression.")
        return

    title = input("Enter graph title: ")
    x_title = input("Label x-axis (explanatory): ")
    y_title = input("Label y-axis (response): ")

    stats_values = graph_and_calc_stats(
        countries_x, countries_y, title, x_title, y_title
    )

    print("Sample Size: " + str(len(countries_x)))
    for key, value in stats_values.items():
        print(key, value)


if __name__ == "__main__":
    main()
