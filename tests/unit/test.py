dictionary = {1 : 1, 3 : 4, 5 : 7, 7 : 10, 9 : 13}
e = enumerate(dictionary)
d = []
for i in e:
 d.append(dictionary[i])
print(d)