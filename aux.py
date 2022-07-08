def dica(temperatura,umidade,vento):
    temperatura = float(temperatura)
    umidade = int(umidade)
    vento = float(vento)

    if umidade > 80:
        dica1 = 'Leve um guarda-chuva'
    elif umidade < 30:
        dica1 = 'Beba água nesse clima seco'
    else:
        dica1 = 'A umidade está ótima'

    if temperatura > 30:
        return dica1 + ' e fique na sombra, está muito quente'
    elif temperatura > 25:
        return dica1 + ' e use roupas leves, dia quente'
    elif temperatura > 20 and vento < 30:
        return dica1 + ' e aproveite o dia, a temperatura está ótima'
    elif temperatura > 20 and vento > 30:
        return dica1 + ' e use roupas longas, o dia está ótimo'
    elif temperatura > 15 and vento < 30:
        return dica1 + ' e se prepare para o frio, use casaco leve'
    elif temperatura > 15 and vento > 30:
        return dica1 + ' e se prepare para o frio, use casaco e touca'
    elif temperatura > 10 and vento < 30:
        return dica1 + ', aproveite o dia frio com uma bebida quente'
    elif temperatura > 10 and vento > 30:
        return dica1 + ', aproveite o dia frio e use touca e luvas'
    elif temperatura > 0:
        return dica1 + ' e se prepare para o frio intenso'
    else:
        return 'Temperatura abaixo de zero, tente ficar em casa'
        
