import pandas as pd

def load_data_from_excel(file_path):
    """
    Lädt Daten aus einer Excel-Datei.
    Die Excel-Datei sollte folgende Blätter enthalten:
    - 'Currents': Ströme in jedem Szenario
    - 'Current Angles': Winkel der Ströme in jedem Szenario
    - 'UNN': UNN-Wert für jedes Szenario
    - 'Voltages': Spannungswerte für jedes Szenario
    - 'INN': INN-Wert für jedes Szenario

    Parameter:
    file_path: str, Pfad zur Excel-Datei

    Rückgabewert:
    Ein Dictionary mit den geladenen Daten.
    """
    # Excel-Datei laden
    xls = pd.ExcelFile(file_path)

    # Daten aus den verschiedenen Blättern laden
    currents_df = pd.read_excel(xls, 'Currents')
    currents_df = currents_df.iloc[:, 1:].astype('float64').fillna(0.0)  # Ersetze NaN durch 0.0 und setze Typ auf float64
    currents = currents_df.T.values.tolist()

    angles_df = pd.read_excel(xls, 'Current Angles')
    angles_df = angles_df.iloc[:, 1:].astype('float64').fillna(0.0)  # Ersetze NaN durch 0.0 und setze Typ auf float64
    angles = angles_df.T.values.tolist()

    unn_values_df = pd.read_excel(xls, 'UNN')
    unn_values_df = unn_values_df.iloc[0, 1:].astype('float64').fillna(0.0)  # Ersetze NaN durch 0.0 und setze Typ auf float64
    unn_values = unn_values_df.tolist()

    voltages_df = pd.read_excel(xls, 'Voltages')
    voltages_df = voltages_df.iloc[:, 1:].astype('float64').fillna(0.0)  # Ersetze NaN durch 0.0 und setze Typ auf float64
    voltages = voltages_df.T.values.tolist()

    inn_values_df = pd.read_excel(xls, 'INN')
    inn_values_df = inn_values_df.iloc[0, 1:].astype('float64').fillna(0.0)  # Ersetze NaN durch 0.0 und setze Typ auf float64
    inn_values = inn_values_df.tolist()

    # Daten in ein Dictionary packen
    data = {
        'currents': currents,
        'angles': angles,
        'unn_values': unn_values,
        'voltages': voltages,
        'inn_values': inn_values
    }

    return data