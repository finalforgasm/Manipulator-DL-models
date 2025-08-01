# -*- coding: utf-8 -*-
"""Visualizing manipulator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e2zqE0zu9Tqnsz_ByWaKeY5qkjcks9sE
"""

import numpy as np
import plotly.graph_objects as go

def dh_transform(a, alpha, d, theta):
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,      sa,     ca,    d],
        [0,       0,      0,    1]
    ])

def generate_colors():
    return ['#FF3C3C', '#FFAA00', '#FFD700', '#00CC99', '#00BFFF', '#9370DB', '#FF69B4']

# DH parameters (scaled for size)
dh_params = [
    [0,      np.pi/2,  2.0,  np.pi/6],
    [1.0,    0,        0,    -np.pi/4],
    [1.0,    0,        0,     np.pi/4],
    [0.6,    np.pi/2,  0,     np.pi/3],
    [0,     -np.pi/2,  1.2,   np.pi/4],
    [0,      np.pi/2,  0,    -np.pi/6],
    [0,      0,        0.6,   np.pi/6],
]

T = np.eye(4)
positions = [T[:3, 3]]
frames = [T]
colors = generate_colors()

for a, alpha, d, theta in dh_params:
    A = dh_transform(a, alpha, d, theta)
    T = T @ A
    positions.append(T[:3, 3])
    frames.append(T)

positions = np.array(positions)

fig = go.Figure()

# Add links
for i in range(len(positions)-1):
    fig.add_trace(go.Scatter3d(
        x=[positions[i,0], positions[i+1,0]],
        y=[positions[i,1], positions[i+1,1]],
        z=[positions[i,2], positions[i+1,2]],
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=16),
        hoverinfo='skip',
        showlegend=False
    ))

# Add joint spheres
fig.add_trace(go.Scatter3d(
    x=positions[:,0], y=positions[:,1], z=positions[:,2],
    mode='markers',
    marker=dict(size=11, color='white', line=dict(color='cyan', width=4)),
    hoverinfo='skip',
    showlegend=False
))

# Add coordinate axes at joints
for T in frames:
    origin = T[:3, 3]
    scale = 0.35
    for vec, color in zip(T[:3,:3].T, ['red', 'green', 'blue']):
        tip = origin + vec * scale
        fig.add_trace(go.Scatter3d(
            x=[origin[0], tip[0]],
            y=[origin[1], tip[1]],
            z=[origin[2], tip[2]],
            mode='lines',
            line=dict(color=color, width=10),
            hoverinfo='skip',
            showlegend=False
        ))

# Layout: Side View
fig.update_layout(
    title="💥 Stylized 7-DOF Robotic Arm – Side View",
    scene=dict(
        xaxis=dict(title='X', backgroundcolor='black', gridcolor='gray', zerolinecolor='white'),
        yaxis=dict(title='Y', backgroundcolor='black', gridcolor='gray', zerolinecolor='white'),
        zaxis=dict(title='Z', backgroundcolor='black', gridcolor='gray', zerolinecolor='white'),
        camera=dict(eye=dict(x=0.1, y=5.5, z=1.8)),
        aspectmode='manual',
        aspectratio=dict(x=1.2, y=1.5, z=1.2)
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(l=0, r=0, b=0, t=60)
)

fig.show()