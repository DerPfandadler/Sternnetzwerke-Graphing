import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Calculate the angle (in degrees) between two points
def calculate_angle(x1, y1, x2, y2):
    """
    Calculate the angle (in degrees) between two points.
    
    Parameters:
    x1, y1, x2, y2: Coordinates of the two points.
    
    Returns:
    Angle in degrees between the two points.
    """
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

# Calculate the quadratic deviations of the distances for the given point p
def combined_distance_error(p, triangle_pts, u_nn, u_values):
    """
    Calculate the quadratic deviations of the distances for the given point.
    
    Parameters:
    p: Coordinates of the point.
    triangle_pts: Coordinates of the triangle vertices.
    u_nn: Distance from the origin to the point.
    u_values: Distances from triangle vertices to the point.
    
    Returns:
    Sum of squared errors of distances.
    """
    x, y = p
    # Distance from N to p
    dist_n = abs(np.sqrt((x - 0) ** 2 + (y - 0) ** 2) - u_nn)
    # Distances from the triangle points L1, L2, L3 to p
    dist_errors = [abs(np.sqrt((x - pt[0]) ** 2 + (y - pt[1]) ** 2) - u_value) for pt, u_value in zip(triangle_pts, u_values)]
    # Sum of squared errors
    return dist_n ** 2 + sum(dist ** 2 for dist in dist_errors)

# Calculate the vertices of the equilateral triangle based on the amplitude of the input voltages
def calculate_triangle_points(triangle_amplitude):
    """
    Calculate the vertices of an equilateral triangle based on the amplitude of the input voltages.
    
    Parameters:
    triangle_amplitude: Amplitude of the input voltages.
    
    Returns:
    List of coordinates of the triangle vertices.
    """
    return [
        (triangle_amplitude * np.cos(np.radians(0)), triangle_amplitude * np.sin(np.radians(0))),
        (triangle_amplitude * np.cos(np.radians(120)), triangle_amplitude * np.sin(np.radians(120))),
        (triangle_amplitude * np.cos(np.radians(240)), triangle_amplitude * np.sin(np.radians(240)))
    ]

# Calculate the optimal point N' by minimizing the distance error
def calculate_optimal_n_prime(triangle_pts, u_nn, u_values):
    """
    Calculate the optimal point N' by minimizing the distance error.
    
    Parameters:
    triangle_pts: Coordinates of the triangle vertices.
    u_nn: Distance from the origin to the point.
    u_values: Distances from triangle vertices to the point.
    
    Returns:
    Coordinates of the optimal point N'.
    """
    centroid = np.mean(triangle_pts, axis=0)  # Calculate centroid of the triangle using NumPy
    initial_guess = (centroid[0], centroid[1])  # Initial guess for optimization based on the centroid
    result = minimize(combined_distance_error, initial_guess, args=(triangle_pts, u_nn, u_values), method='Powell', options={'maxiter': 1000, 'disp': True})
    if not result.success:
        print("Warning: Optimization unsuccessful. Setting N' to centroid.")
        return centroid
    return result.x

# Calculate the angle of I_NN based on the given currents and angles
def calculate_inn_angle(currents, current_angles):
    """
    Calculate the angle of I_NN based on the given currents and angles.
    
    Parameters:
    currents: List of current magnitudes.
    current_angles: List of current angles in degrees.
    
    Returns:
    Angle of I_NN in degrees.
    """
    real_sum = sum(current * np.cos(np.radians(angle)) for current, angle in zip(currents, current_angles))
    imag_sum = sum(current * np.sin(np.radians(angle)) for current, angle in zip(currents, current_angles))
    return np.degrees(np.arctan2(imag_sum, real_sum))

# Plot the diagram of the triangle, star point, and currents
def plot_diagram(triangle_pts, optimal_n_prime, angles, currents, current_angles, inn_value, inn_angle, current_scale=1, shift_enabled=True, ax=None, label_fontsize=10):
    """
    Draw the complete diagram for a scenario.
    Optionally considers star point displacement. If not enabled, N' remains at N.
    
    Parameters:
    triangle_pts: Coordinates of the triangle vertices.
    optimal_n_prime: Coordinates of the optimal point N'.
    angles: List of voltage angles.
    currents: List of current magnitudes.
    current_angles: List of current angles in degrees.
    inn_value: Magnitude of I_NN.
    inn_angle: Angle of I_NN in degrees.
    current_scale: Scaling factor for currents.
    shift_enabled: Boolean indicating if star point displacement is enabled.
    ax: Matplotlib axis to plot on.
    label_fontsize: Font size for labels.
    """


    if ax is None:  # If no axis is provided, create a new one
        _, ax = plt.subplots(figsize=(16, 16))
    else:
        ax.clear()

    # List for text annotations
    texts = []

    # Draw point N
    ax.plot(0, 0, 'bo', markersize=5, label="Star Point N")
    texts.append(ax.text(0, 0, 'N', fontsize=label_fontsize, verticalalignment='bottom', horizontalalignment='right'))

    # Draw N' (only if displacement is enabled)
    if shift_enabled:
        ax.plot(optimal_n_prime[0], optimal_n_prime[1], 'ko', markersize=5)
        texts.append(ax.text(optimal_n_prime[0], optimal_n_prime[1], "N'", fontsize=label_fontsize, verticalalignment='bottom', horizontalalignment='left'))

        # Draw U_NN
        ax.annotate('', xy=(optimal_n_prime[0], optimal_n_prime[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='green'))
        texts.append(ax.text((0 + optimal_n_prime[0]) / 2, (0 + optimal_n_prime[1]) / 2, "U_NN", fontsize=label_fontsize, color='black', ha='center'))

    # Draw the triangle
    triangle = plt.Polygon(triangle_pts, fill=None, edgecolor='orange', linestyle='--')
    ax.add_artist(triangle)

    # Draw L1, L2, L3
    for i, point in enumerate(triangle_pts, start=1):
        ax.plot(point[0], point[1], 'ko')
        texts.append(ax.text(point[0], point[1], f"L{i}", fontsize=label_fontsize, verticalalignment='bottom', horizontalalignment='right'))

    # Draw the voltages U1_2, U2_3, U3_1 (correctly between the points)
    for i in range(3):
        start_point = triangle_pts[i]
        end_point = triangle_pts[(i + 1) % 3]
        mid_x = (start_point[0] + end_point[0]) / 2
        mid_y = (start_point[1] + end_point[1]) / 2

        # Draw the arrow between the points
        ax.annotate('', xy=end_point, xytext=start_point, arrowprops=dict(arrowstyle="->", color='blue'))
        texts.append(ax.text(mid_x, mid_y, f"U{i + 1}_{(i + 2) if (i + 2) <= 3 else 1}", fontsize=label_fontsize, color='blue', ha='center'))

    # Use ax.margins() to automatically add buffer to the axes
    ax.margins(0.1)

    # Lists for legends
    voltage_legend = []
    current_legend = []
    clipped = False  # Flag for shortened arrows

    # Draw voltage angles
    for i, point in enumerate(triangle_pts, start=1):
        ax.annotate('', xy=(point[0], point[1]), xytext=(optimal_n_prime[0], optimal_n_prime[1]), arrowprops=dict(arrowstyle="->", color='green'))
        texts.append(ax.text((point[0] + optimal_n_prime[0]) / 2, (point[1] + optimal_n_prime[1]) / 2, f"U{i}_N'", fontsize=label_fontsize, color='black', ha='center'))

        # Add to voltage legend
        voltage_legend.append(plt.Line2D([0], [0], color='green', linestyle='-', label=f"U{i}_N' ({angles[i-1]:.2f}°)"))

    # Draw currents
    clipped = draw_currents(ax, optimal_n_prime, currents, current_angles, current_scale, label_fontsize, current_legend, current_label_prefix="I", current_color='red')

    # Draw current I_NN with the measured value and angle (only if I_NN exists)
    if inn_value > 0:
        clipped = draw_currents(ax, optimal_n_prime, [inn_value], [inn_angle], current_scale, label_fontsize, current_legend, current_label_prefix="I_NN", current_color='purple')

    ax.set_xticks([])
    ax.set_yticks([])
    plt.grid(False)
    ax.set_aspect('equal', adjustable='box')

    # Add legends
    main_legend = [
        plt.Line2D([0], [0], marker='o', color='blue', linestyle='None', markersize=8, label='Star Point N')
    ]
    if clipped:
        main_legend.append(plt.Line2D([0], [0], color='black', linestyle='dashed', label='Shortened Arrow'))

    ax.legend(handles=main_legend + voltage_legend + current_legend, loc="upper right", fontsize=label_fontsize)

    plt.tight_layout()

# Draw currents with limitation
def draw_currents(ax, optimal_n_prime, currents, current_angles, current_scale, label_fontsize, current_legend, current_label_prefix, current_color):
    """
    Draw the currents with optional limitation based on axis boundaries.
    
    Parameters:
    ax: Matplotlib axis to draw on.
    optimal_n_prime: Coordinates of the optimal point N'.
    currents: List of current magnitudes.
    current_angles: List of current angles in degrees.
    current_scale: Scaling factor for currents.
    label_fontsize: Font size for labels.
    current_legend: List to store legend entries for currents.
    current_label_prefix: Prefix for current labels.
    current_color: Color for current arrows.
    """

    clipped = False

    for i, (current, angle) in enumerate(zip(currents, current_angles), start=1):
        scaled_current = current / current_scale
        dx = scaled_current * np.cos(np.radians(angle))
        dy = scaled_current * np.sin(np.radians(angle))
        end_x = optimal_n_prime[0] + dx
        end_y = optimal_n_prime[1] + dy

        # Check if the arrow needs to be shortened
        linestyle = 'solid'
        if dx != 0 or dy != 0:
            scale = np.inf
            if dx != 0:
                scale = min(scale, (ax.get_xlim()[1] - optimal_n_prime[0]) / dx if dx > 0 else (ax.get_xlim()[0] - optimal_n_prime[0]) / dx)
            if dy != 0:
                scale = min(scale, (ax.get_ylim()[1] - optimal_n_prime[1]) / dy if dy > 0 else (ax.get_ylim()[0] - optimal_n_prime[1]) / dy)

            if scale < 1:
                end_x = optimal_n_prime[0] + dx * scale
                end_y = optimal_n_prime[1] + dy * scale
                linestyle = 'dashed'  # Change style for shortened arrows
                clipped = True

        # Draw the arrow
        if np.isfinite(end_x) and np.isfinite(end_y):
            ax.annotate('', xy=(end_x, end_y), xytext=(optimal_n_prime[0], optimal_n_prime[1]),
                        arrowprops=dict(arrowstyle="->", linestyle=linestyle, color=current_color))
            ax.text((optimal_n_prime[0] + end_x) / 2, (optimal_n_prime[1] + end_y) / 2, f"{current_label_prefix}{i if len(currents) > 1 else ''}", fontsize=label_fontsize, color='black', ha='center')

        # Add to current legend
        current_legend.append(plt.Line2D([0], [0], color=current_color, linestyle=linestyle, label=f"{current_label_prefix} ({angle:.2f}°)"))
    if clipped:
        return clipped
