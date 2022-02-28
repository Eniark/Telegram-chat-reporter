import sys
from pprint import pprint
from enum import Enum
class Medals(Enum):
    Gold = 0
    Silver = 1
    Bronze = 2

filtered_data = {}
create_file = False
output_file = None
command = sys.argv[2]

if command=="-medals":
    dataset = sys.argv[1]
    country = sys.argv[3]
    olympiad_year = sys.argv[4]
elif command=="-total":
    dataset = sys.argv[1]
    olympiad_year = sys.argv[3]
elif command=="-overall":
    dataset = sys.argv[1]
    countries = sys.argv[3:]
AVAILABLE_COUNTRIES_AND_YEARS = []

def store_countries(file, lst = AVAILABLE_COUNTRIES_AND_YEARS):
    next_line = file.readline()
    while next_line:
        country = next_line.split(";")[7]
        year = next_line.split(";")[9]
        if country not in lst:
            lst.append(country)
        if year not in lst:
            lst.append(year)
        next_line = file.readline()
def check_country_and_year(country, year):
    if country not in AVAILABLE_COUNTRIES_AND_YEARS:
        print("Invalid country")
        quit()
    elif year not in AVAILABLE_COUNTRIES_AND_YEARS:
        print("Invalid year")
        quit()
if sys.argv[2] not in ["-medals", "-total", "-overall"]:
    print("Invalid command input")
    quit()
elif sys.argv[-2] == "-output":
    create_file = True
    output_file = sys.argv[-1]

with open(dataset, "r") as f:
    next_line = f.readline()
    counter = 0
    if command=="-medals":
        store_countries(f)
        check_country_and_year(country, olympiad_year)
        f.seek(1)
        all_medals = {}
        while next_line:
            has_country = country in next_line
            has_correct_year = olympiad_year in next_line
            has_medal = next_line[-3:-1] != "NA"

            if has_country and has_correct_year and has_medal and len(filtered_data)<=10:
                name = next_line.split(";")[1]
                medal = next_line.split(";")[-1][:-1]
                discipline_type = next_line.split(";")[-2]
                filtered_data[name] = [discipline_type, medal]
                print(medal)
                if medal not in all_medals:
                    all_medals[medal] = 1
                else:
                    all_medals[medal] += 1
            next_line = f.readline()

        if len(filtered_data)<10:
            print("Знайдено менше 10 переможців...")
            quit()
        f.seek(0)
        for key in filtered_data:
            name = key
            discipline_type = filtered_data[key][0]
            medal = filtered_data[key][1]
            expression = key + " - " + discipline_type + " - "+ medal
            print(expression)
        print()
        print(f"All medals for {country} in {olympiad_year}:")
        print(all_medals)
        for key in all_medals:
            print(f"{key}", all_medals[key], "|", end=" ")
        if create_file:
            with open(output_file, "w") as f:
                for key in filtered_data:
                    name = key.strip("'")
                    discipline_type = filtered_data[key][0]
                    medal = filtered_data[key][1]
                    expression = key + " - " + discipline_type + " - "+ medal +"\n"
                    f.write(expression)

    elif command=="-total": # counting all
        while next_line:
            next_line = next_line.split(";")
            if next_line[9]==olympiad_year and next_line[-1][:2]!="NA":
                country, medal = next_line[7],next_line[-1][:-1]
                if country not in filtered_data:
                    filtered_data[country]=[0,0,0]
                else:
                    if medal == "Gold":
                        filtered_data[country][Medals.Gold.value] += 1
                    elif medal == "Silver":
                        filtered_data[country][Medals.Silver.value] += 1
                    elif medal == "Bronze":
                        filtered_data[country][Medals.Bronze.value] += 1
            next_line=f.readline()
        print("Country - GOLD - SILVER - BRONZE")
        for key, value in filtered_data.items():
            if any(value):
                print(key, "-", filtered_data[key][Medals.Gold.value], "-", filtered_data[key][Medals.Silver.value], "-", filtered_data[key][Medals.Bronze.value])
    elif command == "-overall":
        filtered_data = filtered_data.fromkeys(countries, 0)
        checked_years = {}
        for i in range(len(countries)):
            if countries[i] not in checked_years:
                checked_years[countries[i]] = {}

        while next_line:
            next_line = next_line.split(";")
            country = next_line[6]
            if "-" in country:
                country = next_line[6][:next_line[6].find("-")]
            else:
                year = next_line[9]
            if country in checked_years:
                if year not in checked_years[country]:
                    checked_years[country][year] = 1
                else:
                    checked_years[country][year] += 1
            next_line = f.readline()

        for dkey, val in checked_years.items():
            years_dictionary = checked_years[dkey]
            if len(years_dictionary)==0:
                checked_years[dkey] = "Not found"
                continue
            checked_years[dkey]=dict({max(years_dictionary, key=years_dictionary.get) : years_dictionary[max(years_dictionary, key=years_dictionary.get)]})
        print("Роки, коли задані країни здобули найбільше медалей:")
        pprint(checked_years, width=20)
