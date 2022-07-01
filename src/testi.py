

string = "peruna   porkkana   sipuli"

lista = string.split()
print(lista)

formatted_lista = []
print(lista)

for i in range(len(lista)):
    formatted_lista.append(lista[i])
    formatted_lista.append("")
    formatted_lista.append("")

print(formatted_lista)


