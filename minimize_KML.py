import xml.etree.ElementTree as ET
import sys

def round_coordinates_in_kml(kml_file, output_file):
    # Define the KML namespace
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    # Parse the KML file
    tree = ET.parse(kml_file)
    root = tree.getroot()

    # Iterate over all coordinates elements in the KML (for points, paths, polygons, etc.)
    for coord in root.findall('.//kml:coordinates', ns):
        coords = coord.text.strip()
        # Split the coordinates by spaces (each space represents one coordinate)
        coord_list = coords.split()

        # Round each latitude and longitude to 5 decimals
        rounded_coords = []
        for c in coord_list:
            lon, lat, *rest = c.split(',')
            lon = round(float(lon), 5)
            lat = round(float(lat), 5)
            # Rebuild the coordinate (it may have elevation, which we're keeping)
            rounded_coords.append(f"{lon},{lat},{','.join(rest)}" if rest else f"{lon},{lat}")

        # Join the rounded coordinates back together with spaces
        coord.text = " ".join(rounded_coords)

    # Save the modified KML to the output file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python minimize_KML.py <input KML file> <output KML file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    round_coordinates_in_kml(input_file, output_file)
    print(f"Processed KML saved to {output_file}")

if __name__ == "__main__":
    main()
