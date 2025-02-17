from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "numpy", "cv2", "dlib", "pandas", "PIL", "flask", "sqlite3", "logging"],
    "excludes": ["tkinter.test", "unittest"],
    "include_files": [
        ("data/data_dlib/", "data/data_dlib/"),
        ("templates/", "templates/"),
        ("Icon.ico", "Icon.ico"),
        ("Att.jpg", "Att.jpg")
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
}

executables = [
    Executable(
        script="Main.py",
        target_name="AttendanceSystem.exe",
        icon="Icon.ico",
        base="Win32GUI" if sys.platform == "win32" else None
    ),
    Executable(
        script="Capture.py",
        target_name="Capture.exe",
        base="Win32GUI" if sys.platform == "win32" else None
    ),
    Executable(
        script="Check.py",
        target_name="Check.exe",
        base="Win32GUI" if sys.platform == "win32" else None
    ),
    Executable(
        script="Extract.py",
        target_name="Extract.exe",
        base="Win32GUI" if sys.platform == "win32" else None
    ),
    Executable(
        script="Web.py",
        target_name="Web.exe",
        base="Win32GUI" if sys.platform == "win32" else None
    )
]

setup(
    name="Face Recognition Attendance System",
    version="1.0",
    description="Face Recognition Based Attendance System",
    options={"build_exe": build_exe_options},
    executables=executables
)