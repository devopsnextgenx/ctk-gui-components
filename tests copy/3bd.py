import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 1.0
m_A = 10.0
m_B = 3.0
m_C = 1.0
r = 1.0
s = 0.1

# Initial positions
x_A = -3 * r / 13  # ≈ -0.2308
x_B = 10 * r / 13  # ≈ 0.7692
p_A = np.array([x_A, 0.0])
p_B = np.array([x_B, 0.0])
p_C = np.array([x_B, s])  # C above B

# Initial velocities
omega = np.sqrt(G * (m_A + m_B) / r**3)  # ≈ 3.606
v_A = np.array([0.0, -omega * (3 * r / 13)])  # ≈ [0, -0.832]
v_B = np.array([0.0, omega * (10 * r / 13)])  # ≈ [0, 2.774]
v_rel = np.sqrt(G * m_B / s)  # ≈ 5.477
v_C = v_B + np.array([-v_rel, 0.0])  # ≈ [-5.477, 2.774]

# Acceleration function
def compute_acceleration(p, p1, m1, p2, m2):
    a1 = G * m1 * (p1 - p) / (np.linalg.norm(p1 - p)**3 + 1e-10)  # Avoid division by zero
    a2 = G * m2 * (p2 - p) / (np.linalg.norm(p2 - p)**3 + 1e-10)
    return a1 + a2

# Simulation parameters
dt = 0.001
num_steps = 10000
positions_A, positions_B, positions_C = [], [], []

# Simulation loop
for _ in range(num_steps):
    a_A = compute_acceleration(p_A, p_B, m_B, p_C, m_C)
    a_B = compute_acceleration(p_B, p_A, m_A, p_C, m_C)
    a_C = compute_acceleration(p_C, p_A, m_A, p_B, m_B)
    
    v_A += a_A * dt
    v_B += a_B * dt
    v_C += a_C * dt
    
    p_A += v_A * dt
    p_B += v_B * dt
    p_C += v_C * dt
    
    positions_A.append(p_A.copy())
    positions_B.append(p_B.copy())
    positions_C.append(p_C.copy())

# Plot trajectories
plt.figure(figsize=(8, 8))
plt.plot([p[0] for p in positions_A], [p[1] for p in positions_A], label='A (m=10)')
plt.plot([p[0] for p in positions_B], [p[1] for p in positions_B], label='B (m=3)')
plt.plot([p[0] for p in positions_C], [p[1] for p in positions_C], label='C (m=1)')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('3-Body Simulation: B Orbits A, C Orbits B')
plt.axis('equal')
plt.show()