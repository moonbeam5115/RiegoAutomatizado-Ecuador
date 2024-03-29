import pandas as pd


def promedios_datos_met(path_de_datos):
    data = pd.read_csv(path_de_datos, on_bad_lines='skip')

    estadisticas = data.iloc[0:365].describe()
    t2m_max = estadisticas['T2M_MAX']['mean']
    t2m_min = estadisticas['T2M_MIN']['mean']
    rh2m = estadisticas['RH2M']['mean']
    rh_min = estadisticas['RH2M']['min']
    rh_max = estadisticas['RH2M']['max']

    return t2m_max, t2m_min, rh2m, rh_min, rh_max
