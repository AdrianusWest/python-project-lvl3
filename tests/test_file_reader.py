def read_file(file_path, mode):
    with open(file_path, mode) as data:
        correct_data = data.read()
    return correct_data
