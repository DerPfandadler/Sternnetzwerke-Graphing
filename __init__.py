import os
import subprocess

def main():
    """
    Main function to execute the pointer diagram script.
    - Ensures the required Excel file exists.
    - Provides instructions to the user.
    - Runs the pointer diagram script using subprocess.
    """
    # Dateipfad zur Excel-Datei
    excel_file_path = './data/input.xlsx'

    # Hinweise an den Nutzer
    print(f"Bitte stellen Sie sicher, dass die Excel-Datei {excel_file_path} die folgenden Blätter enthält:")
    print("- 'Currents': Enthält die Ströme für jedes Szenario in separaten Spalten.")
    print("- 'Current Angles': Enthält die Winkel der Ströme für jedes Szenario in separaten Spalten.")
    print("- 'UNN': Enthält den UNN-Wert für jedes Szenario in einer separaten Spalte.")
    print("- 'Voltages': Enthält die Spannungswerte für jedes Szenario in separaten Spalten.")
    print("- 'INN': Enthält den INN-Wert für jedes Szenario in einer separaten Spalte.")
    print("\nBitte füllen Sie die Excel-Datei entsprechend aus und speichern Sie sie ab.")
    print("\n\nWährend der Ausführung des Programms:")
    print("- Sie können durch die individuellen Diagramme navigieren, indem Sie die Pfeiltasten auf Ihrer Tastatur verwenden.")
    print("- Nach dem Schließen des Diagrammfensters wird automatisch eine Zusammenfassung aller Szenarien angezeigt.")
    input("Drücken Sie die Eingabetaste, um fortzufahren...")
    
    if not os.path.exists(os.path.abspath(excel_file_path)):
        print(f"Fehler: Die Datei {excel_file_path} wurde nicht gefunden.")
        return
    
    # Zeigerdigramm-Skript ausführen
    print("\nStarte das Zeigerdiagramm-Skript...")
    try:
        subprocess.run(['python', 'zeigerdiagramme.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Ausführung des Zeigerdiagramm-Skripts: {e}")

if __name__ == "__main__":
    main()
