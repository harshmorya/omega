import numpy as np
import random
import math

def generate_distance_matrix(num_cities):
    # Generate a random distance matrix
    np.random.seed(42)  # For reproducibility
    distances = np.random.randint(1, 100, size=(num_cities, num_cities))
    np.fill_diagonal(distances, 0)  # Diagonal elements are set to 0
    return distances

def total_distance(route, distances):
    # Calculate the total distance of a route
    return sum(distances[route[i], route[i + 1]] for i in range(len(route) - 1)) + distances[route[-1], route[0]]

def generate_initial_solution(num_cities):
    # Generate a random initial solution (permutation of cities)
    return random.sample(range(num_cities), num_cities)

def hill_climbing(current_solution, distances):
    while True:
        neighbors = generate_neighbors(current_solution)
        neighbor_distances = [total_distance(neighbor, distances) for neighbor in neighbors]
        best_neighbor = neighbors[np.argmin(neighbor_distances)]
        if total_distance(best_neighbor, distances) >= total_distance(current_solution, distances):
            break  # If no better solution, terminate
        current_solution = best_neighbor
    return current_solution

def generate_neighbors(solution):
    # Generate neighbors by swapping two random cities
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def simulated_annealing(initial_solution, distances, initial_temperature, cooling_rate):
    current_solution = initial_solution
    temperature = initial_temperature

    while temperature > 1:
        neighbor = random.choice(generate_neighbors(current_solution))
        current_distance = total_distance(current_solution, distances)
        neighbor_distance = total_distance(neighbor, distances)

        if neighbor_distance < current_distance or random.uniform(0, 1) < math.exp((current_distance - neighbor_distance) / temperature):
            current_solution = neighbor

        temperature *= 1 - cooling_rate

    return current_solution

if __name__ == "__main__":
    num_cities = 5
    distance_matrix = generate_distance_matrix(num_cities)

    initial_solution = generate_initial_solution(num_cities)
    print("Initial Solution:", initial_solution)

    # Hill Climbing
    hill_climbing_solution = hill_climbing(initial_solution, distance_matrix)
    print("Hill Climbing Solution:", hill_climbing_solution)
    print("Hill Climbing Total Distance:", total_distance(hill_climbing_solution, distance_matrix))

    # Simulated Annealing
    initial_temperature = 1000
    cooling_rate = 0.003
    sa_solution = simulated_annealing(initial_solution, distance_matrix, initial_temperature, cooling_rate)
    print("Simulated Annealing Solution:", sa_solution)
    print("Simulated Annealing Total Distance:", total_distance(sa_solution, distance_matrix))
