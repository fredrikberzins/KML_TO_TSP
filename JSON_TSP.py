import itertools
import json


def calculate_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][route[0]]  # Return to start
    return total_distance


def tsp_brute_force(distance_matrix, locations, output_file):
    num_locations = len(distance_matrix)
    all_routes = itertools.permutations(range(num_locations))
    shortest_distance = float('inf')
    best_route = None

    for route in all_routes:
        distance = calculate_distance(route, distance_matrix)
        if distance < shortest_distance:
            shortest_distance = distance
            best_route = route
            update_output_file(route, shortest_distance, locations, output_file)
            print(f"New best route: {shortest_distance} -> {format_route(route, locations)}")

    return best_route, shortest_distance


def update_output_file(route, shortest_distance, locations, output_file):
    """Updates the output file with the current best route and distance."""
    result = {
        "route": format_route(route, locations),
        "distance": shortest_distance,
    }
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)


def format_route(route, locations):
    """Formats the route into names and includes direction for paths with start and end."""
    formatted_route = []
    for i in range(len(route) - 1):
        location_name, direction = get_direction(route[i], route[i + 1], locations)
        formatted_route.append(f"{location_name} ({direction})")
    # Add the return to start
    location_name, direction = get_direction(route[-1], route[0], locations)
    formatted_route.append(f"{location_name} ({direction})")
    return formatted_route


def get_direction(from_index, to_index, locations):
    """Determines the direction for paths with start and end."""
    from_name = locations[from_index]
    to_name = locations[to_index]

    if " - start" in from_name and " - end" in to_name:
        return from_name.split(" - ")[0], "start -> end"
    elif " - end" in from_name and " - start" in to_name:
        return from_name.split(" - ")[0], "end -> start"
    else:
        return from_name, "direct"


def parse_distance_matrix(data):
    locations = []

    for entry in data:
        if "point" in entry:
            locations.append(entry["name"])
        elif "start" in entry and "end" in entry:
            locations.append(f"{entry['name']} - start")
            locations.append(f"{entry['name']} - end")

    num_locations = len(locations)
    distance_matrix = [[0] * num_locations for _ in range(num_locations)]

    index = 0
    for entry in data:
        if "point" in entry:
            for j in range(len(entry["point"])):
                distance_matrix[index][j] = entry["point"][j]
            index += 1
        elif "start" in entry and "end" in entry:
            start_distances = entry["start"]
            end_distances = entry["end"]

            for j in range(len(start_distances)):
                distance_matrix[index][j] = start_distances[j]
            index += 1

            for j in range(len(end_distances)):
                distance_matrix[index][j] = end_distances[j]
            index += 1

            # Properly set start-to-end and end-to-start distances
            start_index = index - 2
            end_index = index - 1

            if "length" in entry and isinstance(entry["length"], (int, float)):
                distance_matrix[start_index][end_index] = entry["length"]
                distance_matrix[end_index][start_index] = entry["length"]
            else:
                distance_matrix[start_index][end_index] = float('inf')
                distance_matrix[end_index][start_index] = float('inf')

    return distance_matrix, locations


def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python tsp_brute_force.py <input.json> <output.json>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    distance_matrix, locations = parse_distance_matrix(data)
    best_route, shortest_distance = tsp_brute_force(distance_matrix, locations, output_file)

    print("Final Shortest Route:", format_route(best_route, locations))
    print("Final Shortest Distance:", shortest_distance)


if __name__ == "__main__":
    main()
