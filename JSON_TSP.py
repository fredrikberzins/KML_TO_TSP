import itertools
import json

def calculate_distance(route, distance_matrix, locations, shortest_distance):
    total_distance = 0

    for i in range(len(route) - 1):
        current = locations[route[i]]

        # Validate 'Bulldozer Road(start)' and 'Bulldozer Road(end)' are consecutive
        if '(start)' in current and '(end)' not in locations[route[i + 1]]:
            return float('inf')  # Invalid route
        if '(end)' in current and '(start)' not in locations[route[i - 1]]:
            return float('inf')  # Invalid route

        # Add the distance for the current leg
        total_distance += distance_matrix[route[i]][route[i + 1]]
        
        if total_distance >= shortest_distance:
            return float('inf')
    # Add the distance to return to the starting city
    total_distance += distance_matrix[route[-1]][route[0]]
    
    if total_distance >= shortest_distance:
        return float('inf')

    return total_distance


def tsp_brute_force(distance_matrix, locations, output_file, max_distance):
    num_locations = len(distance_matrix)
    all_routes = itertools.permutations(range(num_locations))
    shortest_distance = max_distance
    best_route = None

    for route in all_routes:
        # Validate and calculate distance in one step
        distance = calculate_distance(route, distance_matrix, locations, shortest_distance)
        if distance < shortest_distance:
            shortest_distance = distance
            best_route = route
            update_output_file(best_route, shortest_distance, locations, output_file)
            print(f"New best route: {shortest_distance} -> {format_route(best_route, locations)}")

    return best_route, shortest_distance


def update_output_file(route, shortest_distance, locations, output_file):
    result = {
        "route": format_route(route, locations),
        "distance": shortest_distance,
    }
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)


def format_route(route, locations):
    formatted_route = []
    for i in range(len(route) - 1):
        location_name = locations[route[i]]
        formatted_route.append(location_name)
    location_name = locations[route[-1]]
    formatted_route.append(location_name)
    return formatted_route


def parse_distance_matrix(data):
    locations = []
    
    for entry in data:
        if "point" in entry:
            locations.append(entry["name"])
        elif "start" in entry and "end" in entry:
            locations.append(f"{entry['name']}(start)")
            locations.append(f"{entry['name']}(end)")

    num_locations = len(locations)
    distance_matrix = [[0] * num_locations for _ in range(num_locations)]

    index = 0
    for entry in data:
        if "point" in entry:
            point = entry["point"]
            for j in range(len(locations)):
                distance_matrix[index][j] = point[j]
            index += 1
        elif "start" in entry and "end" in entry:
            start = entry["start"]
            end = entry["end"]

            start_index = index
            end_index = index + 1

            for j in range(len(start)):
                distance_matrix[start_index][j] = start[j]
            index += 1

            for j in range(len(end)):
                distance_matrix[end_index][j] = end[j]
            index += 1

            if "length" in entry and isinstance(entry["length"], (int, float)):
                length = entry["length"]
                distance_matrix[start_index][end_index] = length
                distance_matrix[end_index][start_index] = length

    return distance_matrix, locations


def main():
    import sys

    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python JSON_TSP.py <input.json> <output.json> [max distance(int)]")
        return
    max_distance = 0
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    max_distance = int(sys.argv[3])

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    distance_matrix, locations = parse_distance_matrix(data)
    print("Locations:", locations)
    print("Distance Matrix:")
    for row in distance_matrix:
        print(row)
    best_route, shortest_distance = tsp_brute_force(distance_matrix, locations, output_file, max_distance)

    print("Final Shortest Route:", format_route(best_route, locations))
    print("Final Shortest Distance:", shortest_distance)


if __name__ == "__main__":
    main()
