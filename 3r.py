# -*- coding: utf-8 -*-
"""3R

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sCgpmIoIMTNdoYzOrOD1ivIvdTh_CCh2
"""

from sympy import symbols, pi, cos, sin, simplify, atan2, acos, sqrt
from sympy.matrices import Matrix
import numpy as np
import math
import matplotlib.pyplot as plt

# Function to create a DH transformation matrix
def build_dh_matrix(theta, alpha, d, a):

    return Matrix([
        [cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
        [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
        [0, sin(alpha), cos(alpha), d],
        [0, 0, 0, 1]
    ])

# Function to compute inverse kinematics for a 3-link planar robot
def inverse_kinematics_3R(x, y, gamma, l1, l2, l3):

    gamma_rad = math.radians(gamma)
    x3 = x - l3 * math.cos(gamma_rad)
    y3 = y - l3 * math.sin(gamma_rad)
    distance = sqrt(x3**2 + y3**2)

    if distance > (l1 + l2):
        print("Target is out of reach.")
        return []

    # Compute angles using cosine law
    cos_theta2 = (x3**2 + y3**2 - l1**2 - l2**2) / (2 * l1 * l2)
    if abs(cos_theta2) > 1:
        print("No valid solution for theta2.")
        return []

    theta2_1 = acos(cos_theta2)
    theta2_2 = -acos(cos_theta2)

    solutions = []
    for theta2 in [theta2_1, theta2_2]:
        k1 = l1 + l2 * math.cos(theta2)
        k2 = l2 * math.sin(theta2)
        theta1 = atan2(y3, x3) - atan2(k2, k1)
        theta3 = gamma_rad - theta1 - theta2
        solutions.append((theta1, theta2, theta3))

    return solutions

def visualize_robot_path_3R(start_point, end_point, gamma, l1, l2, l3, num_steps=50):

    x_path = np.linspace(start_point[0], end_point[0], num_steps)
    y_path = np.linspace(start_point[1], end_point[1], num_steps)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    arm_positions = []
    joint_angles = []

    for x, y in zip(x_path, y_path):
        solutions = inverse_kinematics_3R(x, y, gamma, l1, l2, l3)
        if solutions:
            theta1, theta2, theta3 = solutions[0]  # Use the first solution
            joint_angles.append((theta1, theta2, theta3))

            # Calculate joint positions
            x1 = l1 * math.cos(theta1)
            y1 = l1 * math.sin(theta1)
            x2 = x1 + l2 * math.cos(theta1 + theta2)
            y2 = y1 + l2 * math.sin(theta1 + theta2)
            x3 = x2 + l3 * math.cos(theta1 + theta2 + theta3)
            y3 = y2 + l3 * math.sin(theta1 + theta2 + theta3)

            arm_positions.append(((0, x1, x2, x3), (0, y1, y2, y3)))

    # Plot path
    ax.plot(x_path, y_path, 'b--', label='End Effector Path')

    if arm_positions:
        # Plot start configuration
        start_pos = arm_positions[0]
        ax.plot(start_pos[0], start_pos[1], 'r-', linewidth=2, label='Start Configuration')
        ax.scatter(start_pos[0], start_pos[1], color='r', s=50)

        # Plot end configuration
        end_pos = arm_positions[-1]
        ax.plot(end_pos[0], end_pos[1], 'g-', linewidth=2, label='End Configuration')
        ax.scatter(end_pos[0], end_pos[1], color='g', s=50)

        # Plot intermediate positions
        for pos in arm_positions[1:-1]:
            ax.plot(pos[0], pos[1], 'k-', alpha=0.1)

    ax.set_aspect('equal')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('3-Link Planar Robot Path')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.3)

    # Display joint angles
    if joint_angles:
        start_angles = joint_angles[0]
        end_angles = joint_angles[-1]
        angle_text = f'Start Angles: θ1={math.degrees(start_angles[0]):.1f}°, θ2={math.degrees(start_angles[1]):.1f}°, θ3={math.degrees(start_angles[2]):.1f}°\n'
        angle_text += f'End Angles: θ1={math.degrees(end_angles[0]):.1f}°, θ2={math.degrees(end_angles[1]):.1f}°, θ3={math.degrees(end_angles[2]):.1f}°'
        plt.figtext(0.02, 0.02, angle_text, fontsize=10)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example setup
    l1, l2, l3 = 10, 7, 5
    start_point = (12, 8)
    end_point = (8, 10)
    gamma = 45

    # Visualize the path
    visualize_robot_path_3R(start_point, end_point, gamma, l1, l2, l3)