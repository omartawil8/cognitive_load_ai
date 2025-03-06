import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from PIL import Image

def analyze_cognitive_load(image_path):
    """
    Analyzes cognitive load of a UI screenshot based on contrast, text density, and visual complexity.
    
    - **Contrast**: Measures the difference between light and dark areas. High contrast can improve readability but may strain the eyes if excessive.
    - **Text Density**: Indicates how much text is present. Too much text can overwhelm users, while too little might make the interface unclear.
    - **Unique Colors**: Represents the number of distinct colors used. More colors can add visual interest but may also cause distraction.
    - **Cognitive Load Score**: A combined score estimating how mentally demanding the UI is. A high score suggests the interface may be complex or difficult to process quickly.
    """
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute contrast using Gray Level Co-occurrence Matrix (GLCM)
    glcm = graycomatrix(gray, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
    contrast = round(float(graycoprops(glcm, 'contrast')[0, 0]), 2)

    # Estimate text density (basic approximation via edge detection)
    edges = cv2.Canny(gray, 100, 200)
    text_density = round(float(np.sum(edges) / (gray.shape[0] * gray.shape[1])), 2)

    # Compute number of unique colors (as a proxy for visual complexity)
    unique_colors = len(np.unique(image.reshape(-1, image.shape[2]), axis=0))

    # Heuristic scoring (weighted combination)
    score = round((contrast * 0.4) + (text_density * 0.3) + (unique_colors * 0.3), 2)
    
    # Standardized interpretation with color indicators
    def interpret_value(value, low, high):
        if value < low:
            return ("Low", "🟢", "Clear and easy to read.")  # Green
        elif value > high:
            return ("High", "🔴", "Might be overwhelming or hard to process.")  # Red
        else:
            return ("Moderate", "🟠", "Balanced, but could be optimized.")  # Orange
    
    contrast_level, contrast_color, contrast_desc = interpret_value(contrast, 50, 200)
    text_density_level, text_density_color, text_density_desc = interpret_value(text_density, 0.5, 5)
    unique_colors_level, unique_colors_color, unique_colors_desc = interpret_value(unique_colors, 1000, 50000)
    cognitive_load_level, cognitive_load_color, cognitive_load_desc = interpret_value(score, 3000, 15000)

    return {
        "Contrast": f"{contrast_color} {contrast} ({contrast_level}) - {contrast_desc}",
        "Text Density": f"{text_density_color} {text_density} ({text_density_level}) - {text_density_desc}",
        "Unique Colors": f"{unique_colors_color} {unique_colors} ({unique_colors_level}) - {unique_colors_desc}",
        "Cognitive Load Score": f"{cognitive_load_color} {score} ({cognitive_load_level}) - {cognitive_load_desc}"
    }

# Example Usage:
image_path = "example_ui.png"  # Make sure this file exists
results = analyze_cognitive_load(image_path)
print(results)
