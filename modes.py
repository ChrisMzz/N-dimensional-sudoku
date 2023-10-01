from sudktools import Sudoku



print("Please enter one of these options :")
print("Options :\n - 9x9\n - 9x9 king\n - 9x9 knight\n - 16x16\n - 4x4\n - 4x4x4")
option = input("Your selected option : ")
while option not in ["9x9", "9x9 king", "9x9 knight", "16x16", "4x4", "4x4x4"]:
    option = input("Please select a valid option : ")

if option == "9x9":
    sudk = Sudoku()
elif option == "9x9 king":
    sudk = Sudoku(constraints=['king'])
elif option == "9x9 knight":
    sudk = Sudoku(constraints=['knight'])
elif option == "16x16":
    sudk = Sudoku(N=2, digits=16)
elif option == "4x4":
    sudk = Sudoku(N=2, digits=4)
elif option == "4x4x4":
    sudk = Sudoku(N=3, digits=4)




file = """
<head>
    <link rel="stylesheet" href="fourbyfour.css">
    <script src="fourbyfour.js"></script>
</head>
<body onload="selected=[];addEventListener('keydown', (event) => updateSelection(event));">
    <span class='row'>
        <span class='column'>\n"""
for grid in range(4):
    file += "<table>\n"
    for line in range(4):
        file += "<tr>\n"
        for column in range(4):
            file += f"<td class='cell' id='[{grid},{line},{column}]' onmouseover='highlightCellmates(event)' onmouseleave='unhighlightCellmates(event)' onclick='addToSelection(event)' solution='{sudk.solution[(grid,line,column)]}'>{sudk.grid[(grid,line,column)]}</td>\n"
        file += "</tr>\n"
    file += "</table>\n"
file += """</span>
        <span class='column' style='display:flex;flex-direction: column;justify-content: center;'>"""
file += "<table>\n"
for grid in range(4):
    file += "<tr>\n"
    for column in range(4):
        file += f"<td class='pcell' scope='blue' id='[{grid},b,{column}]'></td>\n"
    file += "</tr>\n"
file += "</table>\n"
file += "<table>\n"
for grid in range(4):
    file += "<tr>\n"
    for line in range(4):
        file += f"<td class='pcell' scope='red' id='[{line},{grid},r]'></td>\n"
    file += "</tr>\n"
file += "</table>\n"
file += """
        </span>
    </span>
</body>"""




with open("youareabitch.html", 'w') as test:
    test.write(file)
