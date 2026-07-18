# Fritzing Custom Parts

This repository contains custom Fritzing parts (.fzpz files) for electronic components.

## Structure

### Custom Parts

- **01_H-Tronic-Solarladeregler** - H-TRONIC Solar Charge Controller
  - `Input/` - Source files (SVG drawings, base parts)
  - `Output/` - Final Fritzing part file (.fzpz)

### Helper Tools

- **00_Helper/01_Image_rotation** - Python script for rotating images (`rotate_image.py`)
- **00_Helper/02_FontsAndTemplates** - Fonts and SVG templates for creating Fritzing parts

#### Fonts

The helper directory includes fonts used in Fritzing part creation:

- **OCR A** - Free OCR-A font based on ANSI X3.17-1977 standard
  - Source: Created from MetaFont definitions using FontForge
  - Installation: Drop `OCRA.ttf` into your system fonts folder, use at 10pt size
  
- **DroidSans** - Android Open Source Project font
  - License: Apache 2.0
  - Installation: Install the TrueType font files to your system fonts folder

#### Templates

SVG templates for creating Fritzing parts are located in `00_Helper/02_FontsAndTemplates/Templates/`:

- `BreadboardViewGraphic_Template.svg` - Template for breadboard view
- `PCBViewGraphic_Template.svg` - Template for PCB view  
- `SchematicViewGraphic_Template.svg` - Template for schematic view

For detailed font information, see `00_Helper/ReadMe.odt`

## Usage

1. Navigate to the desired component folder
2. Find the `.fzpz` file in the `Output/` directory
3. Import the part into Fritzing by dragging it into the application

## File Format

`.fzpz` files are Fritzing part files that can be directly imported into the Fritzing application for use in circuit diagrams, PCB layouts, and breadboard views.
