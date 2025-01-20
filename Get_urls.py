#Input file - id_name_urls.csv
#Output file - urls.csv
import csv
with open('id_name_urls.csv','r') as file:
        csv_reader = csv.reader(file)
#for any other delimiter use csv_reader= csv.reader(file,delimiter=';')
        headers = next(csv_reader)
        for row in csv_reader:
                print(row[2])
                with open('urls.csv','a') as file:
                        file.write(row[2])
                        file.write("\n")                                         
