def reverse_file_content(file_path):
    """
    Read a text file, reverse its content split by spaces, and overwrite the file with the reversed content.
    """
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Reverse the content
        reversed_content = ' '.join(content.split()[::-1])

        # Write the reversed content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(reversed_content)

        print(f"File '{file_path}' has been reversed successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = "temp.txt"
reverse_file_content(file_path)
