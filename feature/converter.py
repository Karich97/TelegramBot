def metric_converter(text):
    text = text.replace(',', '.').strip()
    elements = text.split(' ')
    try:
        amount = float(elements[1])
    except ValueError:
        print(f'metric convert error {elements}')
        return '-1'
    if elements[2] == 'мм':
        inches = 0.0393701 * amount
        return (f'{amount} мм это {round(inches, 2)} в дюймах\n'
                f' или {round(inches / 12, 2)} в футах')
    elif elements[2] == 'см':
        inches = 0.393701 * amount
        return (f'{amount} см это {round(inches, 2)} в дюймах\n'
                f' или {round(inches / 12, 2)} в футах')
    elif elements[2] == 'дм':
        inches = 3.93701 * amount
        return (f'{amount} дм это {round(inches, 2)} в дюймах\n'
                f' или {round(inches / 12, 2)} в футах')
    elif elements[2] == 'км':
        inches = 39370.1 * amount
        return (f'{amount} км это {round(inches / 63360, 2)} в милях \n'
                f' или {round(inches, 2)} в дюймах \n'
                f' или {round(inches / 12, 2)} в футах')
    elif 'дюйм' in elements[2]:
        sm = 2.54 * amount
        return (f'{amount} дюймов это {round(sm, 2)} в сантиметрах\n'
                f' или {round(sm / 100, 2)} в метрах')
    elif 'фут' in elements[2]:
        sm = 30.48 * amount
        return (f'{amount} футов это {round(sm, 2)} в сантиметрах\n'
                f' или {round(sm / 100, 2)} в метрах')
    elif 'мил' in elements[2]:
        sm = 160934 * amount
        return (f'{amount} миль это {round(sm / 100000, 2)} в километрах \n'
                f' или {round(sm, 2)} в сантиметрах \n'
                f' или {round(sm / 100, 2)} в метрах')
    else:
        inches = amount * 39.3701
        return (f'{amount} метров {round(inches, 2)} в дюймах \n'
                f' или {round(inches / 63360, 2)} в милях \n'
                f' или {round(inches / 12, 2)} в футах')