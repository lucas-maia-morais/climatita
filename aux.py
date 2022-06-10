def dica(temperatura):
    temperatura = float(temperatura)
    if temperatura > 25:
        return 'Use roupas leves e aproveite o dia quente'
    elif temperatura > 20:
        return 'Aproveite o dia para caminhar, a temperatura está ótima'
    elif temperatura > 15:
        return 'Se prepare para o frio, use um casaco leve'
    elif temperatura > 10:
        return 'Aproveite o dia frio e tome um chocolate quente'
    elif temperatura > 5:
        return 'Não saia por aí sem roupas adequadas para o frio intenso'
    else:
        return 'Temperatura abaixo de zero, tente ficar em casa'
        
