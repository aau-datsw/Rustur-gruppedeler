# Rustur-gruppedeler

rustrur-gruppedeler.py is a program that reads a CSV file, and creates new groups with x amount of duplicates, and futhuremore attemps to use simulated annealing to minimize the amount of "interconnected" groups
Example of "interconnected" groups:
Group 1 contains student: A1, B1, C1
Group 2 contains student: A2, B2, C2
...
Group 10 contains student: A10, B10, C10

"interconnected" groups would in this case be groups containing:
A1, A2, A3
B1, B2, B3

CSV formate: 
The CSV reader expects the CSV file to use "," as delimiter.
Example of CSV setup:
Group 1, a, b, c...
Group 2, a, b, c...
Group 3, a, b, c...
...
group x, a, b, c...

The CSV file is at the moment hardcoded as a global variable in the top of rustrur-gruppedeler.py, feel free to change this.

Worth noting:
The amount of P0-groups might be higher then the groups you wanna make for the Rustur, therefore the method "contains_duplicates" allows some duplicates in a group.

Output:
When the program is done running, it will output a new CSV file. Due to the lack of time, the program has not been tested, so take a closer look at the output, and maybe make some manual swaps.

<3 GL HF <3
