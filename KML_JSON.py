import json
from xml.etree import ElementTree as ET
import math


# Haversine formula to calculate distance between two lat-long points
def haversine(lat1, lon1, lat2, lon2):
  # Radius of Earth in kilometers
  R = 6371.0

  # Convert latitude and longitude from degrees to radians
  lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

  # Haversine formula
  dlat = lat2 - lat1
  dlon = lon2 - lon1
  a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

  # Calculate distance
  distance = R * c
  return distance


# Helper class to represent a named location (point or path)
class NamedLocation:
  def __init__(self, name, start_lat=None, start_lon=None, end_lat=None, end_lon=None, point_lat=None, point_lon=None):
    self.name = name
    self.start_lat = start_lat
    self.start_lon = start_lon
    self.end_lat = end_lat
    self.end_lon = end_lon
    self.point_lat = point_lat
    self.point_lon = point_lon
    self.length = None  # Length will be calculated for paths

    if self.start_lat is not None and self.end_lat is not None:
      # Calculate the length (distance) if it's a path
      self.length = round(haversine(self.start_lat, self.start_lon, self.end_lat, self.end_lon), 2)

  def to_dict(self):
    if self.point_lat is not None and self.point_lon is not None:
      return {
        "name": self.name,
        "point": {"latitude": self.point_lat, "longitude": self.point_lon}
      }
    else:
      path_data = {
        "name": self.name,
        "start": {"latitude": self.start_lat, "longitude": self.start_lon},
        "end": {"latitude": self.end_lat, "longitude": self.end_lon}
      }
      if self.length is not None:
        path_data["length"] = self.length
      return path_data


# Method to round to 6 decimal places
def round_to_6_decimal_places(value):
  return round(value, 6)


# Method to extract named locations from KML
def extract_named_locations_from_kml(kml_file_name):
  named_locations = []
  try:
    # Parse the KML file with UTF-8 encoding
    with open(kml_file_name, "r", encoding="utf-8") as file:
      tree = ET.parse(file)
      root = tree.getroot()

    # Define namespaces (adjust as needed for your KML file)
    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    for placemark in root.findall(".//kml:Placemark", ns):
      name_element = placemark.find("kml:name", ns)
      name = name_element.text.strip() if name_element is not None else ""

      coordinates_element = placemark.find(".//kml:coordinates", ns)
      if coordinates_element is not None:
        coordinates_text = coordinates_element.text.strip()
        coordinate_pairs = coordinates_text.split()

        if len(coordinate_pairs) == 1:
          # Single point
          lon, lat, *_ = map(float, coordinate_pairs[0].split(","))
          point_lat = round_to_6_decimal_places(lat)
          point_lon = round_to_6_decimal_places(lon)
          named_locations.append(NamedLocation(name, point_lat=point_lat, point_lon=point_lon))
        else:
          # Path with start and end
          first_coord = list(map(float, coordinate_pairs[0].split(",")))
          last_coord = list(map(float, coordinate_pairs[-1].split(",")))

          start_lat = round_to_6_decimal_places(first_coord[1])
          start_lon = round_to_6_decimal_places(first_coord[0])
          end_lat = round_to_6_decimal_places(last_coord[1])
          end_lon = round_to_6_decimal_places(last_coord[0])

          named_locations.append(NamedLocation(name, start_lat=start_lat, start_lon=start_lon,
                                                end_lat=end_lat, end_lon=end_lon))
  except Exception as e:
    print(f"Error: {e}")
  return named_locations


# Method to save named locations to a JSON file
def save_named_locations_to_json(named_locations, json_file_name):
  try:
    # Write JSON with UTF-8 encoding
    with open(json_file_name, "w", encoding="utf-8") as file:
      json.dump([loc.to_dict() for loc in named_locations], file, indent=2, ensure_ascii=False)
    print(f"Named locations saved to {json_file_name}")
  except Exception as e:
    print(f"Error: {e}")


# Main function
def main():
  import sys
  if len(sys.argv) != 3:
    print("Usage: python KML_JSON.py <KML file> <output JSON file>")
    return

  input_file = sys.argv[1]
  output_file = sys.argv[2]

  # Extract named locations from the KML file
  named_locations = extract_named_locations_from_kml(input_file)

  # Save named locations to a JSON file
  save_named_locations_to_json(named_locations, output_file)


if __name__ == "__main__":
  main()
