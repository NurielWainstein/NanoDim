Python-based application for managing STL files. It allows users to upload, and view 3D models, with features such as scaling, rotating, and projecting 3D models to 2D. Built using PyQt6 for the GUI and various Python libraries for 3D and image processing.

Features
STL File Management: Upload, view, and organize STL files.
3D Model Viewer: Rotate and zoom in and out of the model.
3D to 2D Projection: Convert 3D models into 2D images for analysis and further processing.
Image Processing: Use OpenCV for filters and processing on the 2D projections. -> Batch opperations over all the files with multirheading

Modular Architecture: The application is designed with modular components to separate views, models, and controllers.


Installation
Clone the repository:

git clone https://github.com/yourusername/nanodim.git
cd nanodim
Set up the virtual environment:

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Usage
Run the application:
python init_app.py

Navigate the UI:

Use the File Manager to browse and open STL files.
Use the STL File Editor to manipulate the model (scale, rotate, apply filters).
The Image Folder can be used to view 2D projections and apply OpenCV filters.

Project Structure
NanoDim/
├── config.json           # Configuration settings
├── generate_exe.py       # start of a windows installer generator(still not fully working)
├── init_app.py           # Entry point for the application
├── local_files/
│   ├── screenshots      # Directory for saving image outputs
│   ├── stl_files        # Directory for storing STL files
├── requirements.txt     # List of dependencies
├── utils/               # Utility functions and helpers
├── views/               # Screens and views for the app
├── widgets/             # Reusable widgets (dropdowns, file trees, etc.)
└── README.md            # Project documentation
