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
    currents = currents_df.iloc[:, 1:].T.values.tolist()

    angles_df = pd.read_excel(xls, 'Current Angles')
    angles = angles_df.iloc[:, 1:].T.values.tolist()

    unn_values_df = pd.read_excel(xls, 'UNN')
    unn_values = unn_values_df.iloc[0, 1:].tolist()

    voltages_df = pd.read_excel(xls, 'Voltages')
    voltages = voltages_df.iloc[:, 1:].T.values.tolist()

    inn_values_df = pd.read_excel(xls, 'INN')
    inn_values = inn_values_df.iloc[0, 1:].tolist()

    # Daten in ein Dictionary packen
    data = {
        'currents': currents,
        'angles': angles,
        'unn_values': unn_values,
        'voltages': voltages,
        'inn_values': inn_values
    }

    return data