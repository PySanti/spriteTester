def numberList(sep, tested_str, number_count):
    """
        Funcion creada para testear cadenas del formato: numero(separador)numero(separador)
        
        En caso de que "tested_str" cumpla con el formato, la funcion retornara una lista con los numeros, en caso contrario, retornara False
    """
    new_feature = tested_str.split(sep)
    if len(new_feature) != number_count:
        return False
    else:
        try:
            for i in range(0, number_count):
                new_feature[i] = int(new_feature[i])
        except:
            return False
        else:
            return new_feature


while 1:
    print(numberList(",", input(""), 3))
