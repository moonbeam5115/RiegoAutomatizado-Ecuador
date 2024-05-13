def _map(x, in_min, in_max, out_min, out_max):
    '''
    x -- valor del sensor

    in_min -- valores obtenidos por experimento
    in_max -- valores obtenidos por experimento

    out_min -- 0
    out_max -- 100

    returns a value between - 0-1
    '''
    return ((x - in_min)*(out_max, out_min) / (in_max - in_min) + out_min)/100
