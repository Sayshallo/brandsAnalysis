import argparse
import csv
import os
import sys

from tabulate import tabulate


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-f', '--files', nargs='+', default=['products1.csv'])
    parser.add_argument ('-r', '--report', default=['result.csv'])
    args = parser.parse_args()

    return args

def read_files(files_path):
    products = list()
    for file in files_path:
        if len(file) < 5:
            print("Слишком короткое название файла!")
            continue
        elif file[-4:].lower() != '.csv':
            print("Не все файлы имеют расширение CSV!", file=sys.stderr)
            continue

        try:
            with open(file, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products.append(row)
        except FileNotFoundError:
            print(f"Файла {file} не существует!", file=sys.stderr)
        except:
            print(f"Произошла ошибка при обработке файла {file}!", file=sys.stderr)

    return del_duplicates(value_normalizer(products))

def del_duplicates(products):
    for idx, value in enumerate(products):
        try:
            cur_name = value["name"].lower()
            for idx_, value_ in enumerate(products):
                if cur_name == value_["name"].lower() and idx != idx_:
                    products.remove(value_)
                    print(value_)
        except KeyError: continue

    return products

def value_normalizer(products):
    for value in products:
        try:
            value["brand"] = value["brand"].lower().strip()
            value["rating"]
            if len(value["brand"]) == 0 or len(value["rating"]) == 0:
                products.remove(value)
                print(f"Была удалена строка {value} из-за наличия в ней пустых значений!")
        except KeyError:
            products.remove(value)
    return products

def calc_avg_rating(products):
    brands_rating = dict()
    for row in products:
        if not check_rating(row): continue
        try: brand = str(row["brand"]).lower()
        except KeyError: continue
        rating = float(row["rating"])
        try:
            brands_rating[brand][0] += rating
            brands_rating[brand][1] += 1
        except KeyError:
            brands_rating[brand] = [rating, 1]

    for brand in brands_rating:
        brands_rating[brand] = round(brands_rating[brand][0] / brands_rating[brand][1], 2)

    return brands_rating

def check_rating(row):
    try:
        rating = float(row["rating"])
        if len(row["rating"]) == 0 or rating is None:
            print(f"В строке {row} значение столбца rating - {row['rating']} является пустым!")
            return False
        elif rating > 5 or rating <= 0:
            print(f"В строке {row} значение столбца rating - {row['rating']} находится вне диапазона 0.0 - 5.0!")
            return False
    except ValueError:
        print(f"В строке {row} значение столбца rating - {row['rating']} не является числом!")
        return False
    except TypeError:
        print(f"В строке {row} значение столбца rating - {row['rating']} не является числом!")
        return False

    return True


def make_report(filename, average_rating):
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['brand', 'rating'])
            writer.writerows(average_rating)
    except FileNotFoundError:
        create_dir(filename)
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['brand', 'rating'])
            writer.writerows(average_rating)
    except FileExistsError:
        create_dir(filename)
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['brand', 'rating'])
            writer.writerows(average_rating)

def create_dir(path):
    if path.find('\\\\'): path.replace('\\\\', '\\')
    path = str(path)[0:str(path).rfind('\\')]
    print(path)
    is_created = False
    while (not is_created):
        try:
            os.mkdir(path)
            is_created = True
        except FileNotFoundError: create_dir(path)


def main():
    args = parse_args()
    products = read_files(args.files)
    average_rating = calc_avg_rating(products)
    unique_brands_rating = sorted(average_rating.items(), key=lambda item: item[1], reverse=True)
    make_report(args.report, unique_brands_rating)
    print(tabulate(unique_brands_rating, headers=['brand', 'rating'], tablefmt="grid"))



if __name__ == "__main__":
    main()
