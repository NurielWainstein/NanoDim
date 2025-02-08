import os
import threading
import cv2

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

def check_and_transpose_image(file_path, **kwargs):
    """
    This function checks if the image width is larger than the height.
    If true, it transposes (rotates) the image and saves it.
    """
    # Read the image
    image = cv2.imread(file_path)
    if image is None:
        print(f"Failed to load image: {file_path}")
        return

    h, w = image.shape[:2]

    if h > w:
        print(f"Image {file_path} is landscape. Transposing...")
        transposed_image = cv2.transpose(image)
        transposed_image = cv2.flip(transposed_image, flipCode=1)

        # Save the transposed image
        cv2.imwrite(file_path, transposed_image)
    else:
        print(f"Image {file_path} is portrait. No changes made.")


def rotate_image(file_path, **kwargs):
    """
    This function rotates an image by the given angle (in kwargs).
    The image is saved in place and the canvas is adjusted to ensure no cropping.
    """
    # Check if 'rotation_angle' is in kwargs
    rotation_angle = kwargs.get('rotation_angle')
    if rotation_angle is None:
        print(f"Rotation angle not provided for image: {file_path}")
        return

    # Read the image
    image = cv2.imread(file_path)
    if image is None:
        print(f"Failed to load image: {file_path}")
        return

    # Get the image dimensions (height, width)
    h, w = image.shape[:2]

    # Get the rotation matrix
    center = (w / 2, h / 2)  # The center of the image
    rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)

    # Calculate the new bounding box size after rotation
    abs_cos = abs(rotation_matrix[0, 0])
    abs_sin = abs(rotation_matrix[0, 1])

    # Calculate the new width and height
    new_w = int(h * abs_sin + w * abs_cos)
    new_h = int(h * abs_cos + w * abs_sin)

    # Adjust the rotation matrix to take into account the translation
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]

    # Rotate the image and resize the canvas
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))

    # Save the rotated image back in place
    cv2.imwrite(file_path, rotated_image)
    print(f"Image rotated by {rotation_angle} degrees and saved in place: {file_path}")
