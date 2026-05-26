import csv
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

from tkinter.filedialog import askopenfilename

country_data = {}

countries_x = []
countries_y = []


def init_country_dict(_name, _year, _data1):
    return dict(name=_name, year=_year, data1=_data1, data2=None)


def fill_data_set(paths: list, year: str):
    for path in paths:
        with open(path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Year"] == year:
                    vlist = list(row.values())

                    if vlist[1] in country_data:
                        country_data[vlist[1]]["data2"] = vlist[3]
                    else:
                        country_data[vlist[1]] = init_country_dict(
                            vlist[1], vlist[2], vlist[3]
                        )


def fill_x_y():
    for code in country_data:
        data = country_data[code]
        countries_x.append(data["data1"])
        countries_y.append(data["data2"])


def purge_unmatched_pairs():
    to_pop = []

    for code in country_data:
        if country_data[code]["data2"] == None:
            to_pop.append(code)
    for code in to_pop:
        country_data.pop(code)

    fill_x_y()


def graph_and_calc_stats_variables():
    countries_x_float = list(map(float, countries_x))
    countries_y_float = list(map(float, countries_y))

    slope, intercept, r, p, std_err = linregress(countries_x_float, countries_y_float)
    r_squared = r**2

    plt.scatter(countries_x_float, countries_y_float)
    plt.plot(countries_x_float, slope * np.array(countries_x_float) + intercept)

    title = input("Enter graph title: ")
    x_title = input("Label x-axis (explanatory): ")
    y_title = input("Label y-axis (response): ")

    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)

    plt.savefig("statscsv/output/graph.png")

    return dict(
        slope=slope, intercept=intercept, r=r, p=p, std_err=std_err, r2=r_squared
    )


def main():
    year = input("Target Year: ")

    explanatory_variables = askopenfilename()
    response_variables = askopenfilename()

    try:
        fill_data_set([explanatory_variables, response_variables], year)
    except Exception as e:
        print("Error Occured")
        print(e)
        return

    purge_unmatched_pairs()
    stats_values = graph_and_calc_stats_variables()

    print("Sample Size: " + str(len(country_data)))

    for key, value in stats_values.items():
        print(key, value)


if __name__ == "__main__":
    main()
