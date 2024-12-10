import json
import sys

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

def calculate_route_distance(route, distance_matrix, locations):
    total_distance = 0

    # Map location names to indices
    location_indices = {name: idx for idx, name in enumerate(locations)}

    # Iterate through the route to calculate distance
    for i in range(len(route) - 1):
        from_location = route[i]
        to_location = route[i + 1]

        from_index = location_indices[from_location]
        to_index = location_indices[to_location]

        total_distance += distance_matrix[from_index][to_index]

    # Add the distance to return to the starting location
    start_index = location_indices[route[0]]
    end_index = location_indices[route[-1]]
    total_distance += distance_matrix[end_index][start_index]

    return total_distance

def main():
    if len(sys.argv) != 4:
        print("Usage: python JSON_TSP.py <input.json> <distance_matrix.json> <output.json>")
        return

    input_file = sys.argv[1]
    distance_matrix_file = sys.argv[2]
    output_file = sys.argv[3]

    # Load the input route and locations from input.json
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Load the pre-existing distance matrix from distance_matrix.json
    with open(distance_matrix_file, "r", encoding="utf-8") as file:
        distance_data = json.load(file)

    # Parse the distance matrix using the existing parser function
    distance_matrix, locations = parse_distance_matrix(distance_data)
    print("Locations:", locations)
    print("Distance Matrix:")

    # Extract the route from the input file
    if "route" not in data:
        print("Error: No 'route' field found in the input JSON.")
        return

    route = data["route"]
    total_distance = calculate_route_distance(route, distance_matrix, locations)

    # Add the distance to the JSON data
    data["distance"] = total_distance

    # Write the updated JSON to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


    print(f"Route distance calculated and saved to {output_file}.")

if __name__ == "__main__":
    main()
