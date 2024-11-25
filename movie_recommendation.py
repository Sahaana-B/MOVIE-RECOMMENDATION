#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Global variable to hold movie data
movie_data = None


def upload_file():
    """Function to upload a CSV file and load the data."""
    global movie_data
    file_path = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not file_path:
        messagebox.showwarning("Warning", "No file selected!")
        return

    try:
        # Try reading the file with UTF-8 encoding
        movie_data = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Fallback to Latin-1 encoding for non-UTF-8 files
        try:
            movie_data = pd.read_csv(file_path, encoding='latin1')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            movie_data = None
            return

    # Strip spaces and normalize column names
    movie_data.columns = movie_data.columns.str.strip().str.lower()

    # Debug: Display detected columns
    print("Detected columns:", movie_data.columns.tolist())

    # Check for required columns
    if 'title' not in movie_data.columns or 'genres' not in movie_data.columns:
        messagebox.showerror("Error", "CSV must contain 'title' and 'genres' columns!")
        movie_data = None
        return

    messagebox.showinfo("Success", "File uploaded successfully!")


def recommend_movies():
    """Function to recommend movies based on genre."""
    global movie_data
    if movie_data is None:
        messagebox.showwarning("Warning", "Please upload a movie dataset first!")
        return

    genre = entry_genre.get().strip().lower()
    if not genre:
        messagebox.showwarning("Warning", "Please enter a genre!")
        return

    # Filter movies that contain the input genre
    recommended = movie_data[movie_data['genres'].str.contains(genre, case=False, na=False)]['title'].tolist()

    if recommended:
        result_text.set("\n".join(recommended))
    else:
        result_text.set("No movies found for this genre.")


# Create the main window
root = tk.Tk()
root.title("Movie Recommendation System")

# Set window dimensions
root.geometry("500x400")  # Width x Height

# Upload file button
tk.Button(root, text="Upload CSV File", command=upload_file, font=("Arial", 12), width=20).pack(pady=20)

# Input field for genre
tk.Label(root, text="Enter a Genre (e.g., Drama, Action):", font=("Arial", 12)).pack(pady=10)
entry_genre = tk.Entry(root, font=("Arial", 12), width=30)
entry_genre.pack(pady=10)

# Get recommendations button
tk.Button(root, text="Get Recommendations", command=recommend_movies, font=("Arial", 12), width=20).pack(pady=20)

# Display recommendations
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", fg="blue", wraplength=450, font=("Arial", 10))
result_label.pack(pady=10)

# Run the GUI
root.mainloop()


# In[ ]:




