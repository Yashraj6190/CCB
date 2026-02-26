import numpy as np

def get_propensities(x1, x2, x3):
    # Propensities based on the discrete probability models provided
    a1 = 0.5 * x1 * (x1 - 1) * x2
    a2 = x1 * x3 * (x3 - 1)
    a3 = 3 * x2 * x3
    return np.array([a1, a2, a3])

def simulate_1a(initial_state, num_steps=100000):
    state = np.array(initial_state)
    counts = {'C1': 0, 'C2': 0, 'C3': 0}
    
    for _ in range(num_steps):
        props = get_propensities(*state)
        a0 = np.sum(props)
        
        if a0 == 0: 
            break # Absorbing state reached
            
        # Check conditions
        if state[0] >= 150: counts['C1'] += 1
        if state[1] < 10: counts['C2'] += 1
        if state[2] > 100: counts['C3'] += 1
        
        # Determine next reaction
        r = np.random.rand() * a0
        # print(f"Current state: {state}, Propensities: {props}, Random number: {r}")
        if r < props[0]:
            state += np.array([-2, -1, 4])
        elif r < props[0] + props[1]:
            state += np.array([-1, 3, -2])
        else:
            state += np.array([2, -1, -1])
        
        # print(f"Updated state: {state}")
            
    # Return estimated probabilities (time-averaged over steps)
    return {k: v / num_steps for k, v in counts.items()}

# Initial state for 1a
initial_state_1a = [110, 26, 55]
probs = simulate_1a(initial_state_1a)
print("Estimated Probabilities:", probs)

def simulate_1b(initial_state, num_trials=100000, target_steps=7):
    final_states = []
    
    for _ in range(num_trials):
        state = np.array(initial_state)
        for _ in range(target_steps):
            props = get_propensities(*state)
            a0 = np.sum(props)
            if a0 == 0: break
            
            r = np.random.rand() * a0
            if r < props[0]:
                state += np.array([-2, -1, 4])
            elif r < props[0] + props[1]:
                state += np.array([-1, 3, -2])
            else:
                state += np.array([2, -1, -1])
        final_states.append(state)
        
    final_states = np.array(final_states)
    
    # Calculate mean and variance for X1, X2, X3
    means = np.mean(final_states, axis=0)
    variances = np.var(final_states, axis=0)
    
    return means, variances

initial_state_1b = [9, 8, 7]
means, variances = simulate_1b(initial_state_1b)
print("Means (X1, X2, X3):", means)
print("Variances (X1, X2, X3):", variances)