import os
import matplotlib.pyplot as plt
from input_excel_data import load_data_from_excel
from plotting_functions import calculate_triangle_points, plot_diagram, calculate_inn_angle, calculate_optimal_n_prime

class ZeigerDiagram:
    def __init__(self):
        self.fig = None
        self.ax = None
        self.current_index = 0
        self.global_label_fontsize = 12      # Standard-Schriftgröße für Labels
        self.overview_label_fontsize = 10     # Standard-Schriftgröße für Labels in der Übersicht
        self.global_triangle_amplitude = 50  # Amplitude des Dreiecks
        self.global_current_scale = 1.5      # Skalierung für die Strompfeile

        # Daten aus der Excel-Datei laden
        data = load_data_from_excel(os.path.abspath('./data/input.xlsx'))

        # INN-Werte für jedes Szenario
        self.inn_values = data['inn_values']

        # Winkel von INN für jedes Szenario (initial leer)
        self.inn_angles = [None] * len(self.inn_values)

        # Ströme für jedes Szenario
        self.currents_scenarios = data['currents']

        # Winkel der Ströme für jedes Szenario
        self.current_angle_scenarios = data['angles']

        # UNN-Werte für jedes Szenario
        self.unn_values = data['unn_values']

        # Spannungswerte für jedes Szenario
        self.voltage_values = data['voltages']

    def on_key(self, event):
        """
        Handhabt die Navigation durch die Szenarien mit den Pfeiltasten.
        """
        if event.key == 'right':  # Nächstes Szenario
            self.current_index = (self.current_index + 1) % len(self.currents_scenarios)
        elif event.key == 'left':  # Vorheriges Szenario
            self.current_index = (self.current_index - 1) % len(self.currents_scenarios)

        # Aktualisiere das Diagramm basierend auf dem neuen Szenario
        self.update_plot()

    def initialize_plot_data(self, index):
        """
        Initialisiert die Werte für das aktuelle Szenario.
        """
        triangle_pts = calculate_triangle_points(self.global_triangle_amplitude)
        current_values = self.currents_scenarios[index]
        current_angles = self.current_angle_scenarios[index]
        u_nn = self.unn_values[index]
        u_values = self.voltage_values[index]
        inn_value = self.inn_values[index]

        # Berechne den Winkel von I_NN, falls noch nicht gesetzt
        if self.inn_angles[index] is None:
            self.inn_angles[index] = calculate_inn_angle(current_values, current_angles)

        # Überprüfe, ob der berechnete Winkel von I_NN None ist, falls ja, setze ihn auf 0
        inn_angle = self.inn_angles[index] if self.inn_angles[index] is not None else 0

        # Prüfe, ob U_NN = 0 ist
        if u_nn == 0 or u_nn is None:
            # Keine Sternpunktverschiebung: N' bleibt N
            optimal_n_prime = (0, 0)
            shift_enabled = False
        else:
            # Berechne den verschobenen Sternpunkt
            optimal_n_prime = calculate_optimal_n_prime(triangle_pts, u_nn, u_values)
            shift_enabled = True

        return triangle_pts, current_values, current_angles, u_values, inn_value, inn_angle, optimal_n_prime, shift_enabled

    def update_plot(self):
        """
        Aktualisiert das individuelle Diagramm basierend auf dem aktuellen Szenario (current_index).
        Falls U_NN = 0, wird keine Sternpunktverschiebung berechnet.
        """
        # Validierung von current_index
        if self.current_index < 0 or self.current_index >= len(self.voltage_values):
            print(f"Warnung: current_index ({self.current_index}) ist außerhalb der gültigen Grenzen. Setze auf 0.")
            self.current_index = 0

        # Falls fig oder ax nicht existieren, erstelle sie
        if self.fig is None or self.ax is None:
            self.fig, self.ax = plt.subplots(figsize=(16, 16))
        else:
            self.ax.clear()  # Lösche den Inhalt der Achse, um sie neu zu zeichnen

        # Initialisiere die Werte für das aktuelle Szenario
        triangle_pts, current_values, current_angles, u_values, inn_value, inn_angle, optimal_n_prime, shift_enabled = self.initialize_plot_data(self.current_index)

        # Zeichne das Diagramm für das aktuelle Szenario
        plot_diagram(
            triangle_pts=triangle_pts,
            optimal_n_prime=optimal_n_prime,
            angles=u_values,
            currents=current_values,
            current_angles=current_angles,
            inn_value=inn_value,
            inn_angle=inn_angle,
            current_scale=self.global_current_scale,
            shift_enabled=shift_enabled,
            ax=self.ax,  # Übergabe der bestehenden Achse
            label_fontsize=self.global_label_fontsize
        )

        # Aktualisiere den Fenstertitel
        self.fig.canvas.manager.set_window_title(f"Zeigerdiagramme - Szenario {self.current_index + 1} von {len(self.currents_scenarios)} (mit Pfeiltasten navigieren)")

        self.fig.canvas.draw_idle()  # Aktualisiere die Anzeige

    def show_overview(self):
        """
        Zeigt eine Übersicht aller Szenarien als Subplots in einem separaten Fenster.
        Passt die Anzahl der Zeilen und Spalten dynamisch an die Anzahl der Szenarien an.
        """
        # Speichere den aktuellen Wert von current_index, um ihn nach der Funktion wiederherzustellen
        original_index = self.current_index

        # Berechne die Anzahl der Szenarien
        num_scenarios = len(self.currents_scenarios)

        # Dynamisch die Anzahl der Spalten und Zeilen festlegen (z. B. maximal 4 Spalten)
        max_cols = 4  # Maximale Anzahl an Spalten
        cols = min(num_scenarios, max_cols)  # Weniger Spalten, wenn Szenarien < max_cols
        rows = (num_scenarios + cols - 1) // cols  # Anzahl der notwendigen Zeilen

        # Erstelle die Figur mit dynamischem Layout
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))  # Größe proportional zur Anzahl der Szenarien anpassen
        fig.subplots_adjust(hspace=0.4, wspace=0.4)  # Abstand zwischen den Subplots

        # Falls es nur eine Zeile gibt, sicherstellen, dass axes iterierbar ist
        if rows == 1:
            axes = [axes] if cols == 1 else axes.flatten()
        else:
            axes = axes.flatten()

        # Iteriere durch jedes Szenario und zeichne es als Subplot
        for idx in range(num_scenarios):
            ax = axes[idx]  # Wähle die aktuelle Achse
            self.current_index = idx  # Setze den aktuellen Index auf das Szenario

            # Initialisiere die Werte für das aktuelle Szenario
            triangle_pts, current_values, current_angles, u_values, inn_value, inn_angle, optimal_n_prime, shift_enabled = self.initialize_plot_data(self.current_index)

            # Zeichne das Diagramm für den Subplot
            plot_diagram(
                triangle_pts=triangle_pts,
                optimal_n_prime=optimal_n_prime,
                angles=u_values,
                currents=current_values,
                current_angles=current_angles,
                inn_value=inn_value,
                inn_angle=inn_angle,
                current_scale=self.global_current_scale,
                shift_enabled=shift_enabled,
                ax=ax,
                label_fontsize=self.overview_label_fontsize
            )

            # Füge einen Titel hinzu
            ax.set_title(f"Szenario {idx + 1}", fontsize=14)

        # Deaktiviere ungenutzte Subplots (falls Szenarien < rows * cols)
        for ax in axes[num_scenarios:]:
            ax.axis('off')

        # Ursprünglichen Index wiederherstellen
        self.current_index = original_index

        plt.show()

# Erstelle eine Instanz von ZeigerDiagram und initialisiere das erste Diagramm
diagram = ZeigerDiagram()
diagram.update_plot()

# Verbinde die Pfeiltasten-Navigation
diagram.fig.canvas.mpl_connect('key_press_event', diagram.on_key)

# Zeige das Diagramm
plt.show()
diagram.show_overview()
