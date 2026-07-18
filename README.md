# Fritzing Custom Parts

This repository contains custom Fritzing parts (.fzpz files) for electronic components.

## Structure

### Custom Parts

- **01_H-Tronic-Solarladeregler** - H-TRONIC Solar Charge Controller
  - `Input/` - Source files (SVG drawings, base parts)
  - `Output/` - Final Fritzing part file (.fzpz)

### Helper Tools

- **00_Helper/01_Image_rotation** - Python script for rotating images (`rotate_image.py`)

## Usage

1. Navigate to the desired component folder
2. Find the `.fzpz` file in the `Output/` directory
3. Import the part into Fritzing by dragging it into the application

## File Format

`.fzpz` files are Fritzing part files that can be directly imported into the Fritzing application for use in circuit diagrams, PCB layouts, and breadboard views.
