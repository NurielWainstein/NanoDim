import os
import threading


def _process_file(file_path, func, **kwargs):
    """
    This function will process a single file with the given function.
    """
    print(f"Processing file: {file_path}")
    func(file_path, **kwargs)


def _process_files_in_directory(directory, func, **kwargs):
    """
    This function will loop over all files in the directory, spawn threads for processing each file.
    """
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    threads = []
    for file_path in files:
        thread = threading.Thread(target=_process_file, args=(file_path, func), kwargs=kwargs)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to complete


# Sample functions you provided
def hello(file_path, **kwargs):
    print(f"Hello from custom function! Processing: {file_path}")


def greet(file_path, **kwargs):
    print(f"Greetings from custom function! Processing: {file_path}")


def process_data(file_path, **kwargs):
    print(f"Processing data for file: {file_path}")
