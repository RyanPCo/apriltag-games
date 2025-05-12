import numpy as np
from scipy.spatial.distance import euclidean

# Templates for simple shapes (normalized, 64 points each)
def generate_circle_template(num_points=64):
    t = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    return np.stack([np.cos(t), np.sin(t)], axis=1)

def generate_triangle_template(num_points=64):
    points = np.array([
        [0, 1],
        [-np.sqrt(3)/2, -0.5],
        [np.sqrt(3)/2, -0.5],
        [0, 1]
    ])
    t = np.linspace(0, 1, num_points)
    segs = [
        (points[i], points[i+1]) for i in range(3)
    ]
    seg_lengths = [np.linalg.norm(b-a) for a, b in segs]
    total = sum(seg_lengths)
    seg_points = []
    for (a, b), l in zip(segs, seg_lengths):
        n = int(np.round(num_points * l / total))
        seg_points.append(np.linspace(a, b, n, endpoint=False))
    triangle = np.concatenate(seg_points)
    return triangle[:num_points]

def generate_line_template(num_points=64):
    return np.linspace([-1, 0], [1, 0], num_points)

TEMPLATES = {
    'circle': generate_circle_template(),
    'triangle': generate_triangle_template(),
    'line': generate_line_template(),
}

def preprocess_path(path, num_points=64):
    path = np.array(path)
    # Center
    path = path - np.mean(path, axis=0)
    # Scale
    max_range = np.max(np.linalg.norm(path, axis=1))
    if max_range > 0:
        path = path / max_range
    # Resample
    idxs = np.linspace(0, len(path)-1, num_points).astype(int)
    path = path[idxs]
    return path

def recognize_symbol(path):
    path = preprocess_path(path)
    min_dist = float('inf')
    best = None
    for name, template in TEMPLATES.items():
        dist = np.mean([euclidean(p, t) for p, t in zip(path, template)])
        if dist < min_dist:
            min_dist = dist
            best = name
    # Threshold for recognition
    if min_dist > 0.5:
        return None
    return best 