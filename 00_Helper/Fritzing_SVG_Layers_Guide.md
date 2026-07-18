# Fritzing SVG Layers Guide - Through-Hole Components

## Overview
This guide explains the layer structure for creating well-engineered plain SVG files for Fritzing PCB through-hole components.

## Layer Names and Functions

### Copper Layers (Precise Definitions)

- **copper1** - **Top copper layer** (Component Placement Side)
  - Through-hole components: Component body is placed on this side
  - SMD components: Placed and soldered on this side
  - This is the side you typically see with component labels
  
- **copper0** - **Bottom copper layer** (Solder Side)
  - Through-hole components: Leads are soldered on this side
  - SMD components: Can also be placed on bottom (double-sided boards)
  - Traditional "solder side" of the PCB

### Other Essential Layers

- **silkscreen** - Component outlines and labels (white text/lines)
  - Typically printed on the **top side** (component side)
  - Shows component boundaries, polarity marks, pin numbers, reference designators (R1, C1, IC1)
  - Can also exist as **silkscreen0** (bottom) for double-sided assemblies
  
**Note:** The official documentation mentions copper0, copper1, and silkscreen layers for component parts. Other layer types may exist but are not documented in the official part file format guide.

### Special IDs (PCB Boards Only)

These are NOT for regular component parts - only for PCB board shapes:

- **id="boardoutline"** - Used to define the contour of a PCB board shape
  - If a board layer has multiple elements, Fritzing chooses the largest by default
  - Adding `id="boardoutline"` to an element forces Fritzing to use that specific element as the board contour
  - Only relevant for custom PCB board shapes (like Arduino shields), not component footprints

### Through-Hole Assembly Process
1. Component placed on **top side** (copper1)
2. Leads protrude through holes
3. Leads soldered on **bottom side** (copper0)
4. Both copper0 and copper1 have the same connector pads for electrical continuity

## Through-Hole Pad Structure

### Connector ID Naming - IMPORTANT!
- **For through-hole pads in Fritzing**: Use the **SAME ID** in both copper0 and copper1 layers
  - Example: `connector0pad` is referenced in BOTH layers in the FZP file
  
- **SVG Structure to avoid duplicate IDs**: Nest copper1 group INSIDE copper0 group
  - This way, the actual shape elements (circles, rects) only appear ONCE in the SVG
  - Fritzing automatically applies them to both layers because of the nesting
  
- **Naming convention** (based on actual Fritzing parts):
  - **PCB View**: `connector0pad`, `connector1pad`, `connector2pad`, etc.
  - **Breadboard View**: `connector0pin`, `connector1pin`, etc. (for the connector area)
  - **Schematic View**: `connector0pin`, `connector1pin`, etc. (for the connector area)
  - **Terminal points**: `connector0terminal`, `connector1terminal`, etc. (optional - defines wire attachment point)

### Understanding connectorXpad, connectorXpin, and connectorXterminal

**From official Fritzing documentation:**

**svgId (connector area):**
- `connectorXpad` (PCB view), `connectorXpin` (breadboard/schematic) - defines the **shape and area** of the connector
- This element determines the visual appearance and clickable region
- Wires attach within this area

**terminalId (wire attachment point) - OPTIONAL:**
- `connectorXterminal` - defines the **specific point** where wires actually attach
- If omitted, wires attach at the **center** of the connector area
- Use this when you want wires to attach at a specific point other than the center

**Example from official documentation:**

Breadboard view connector area:
```xml
<rect id="connector0pin" x="4.793" y="65.307" fill="none" width="2.989" height="9.442"/>
```

Optional terminal point (wire attachment):
```xml
<rect id="connector0terminal" x="4.793" y="74.192" fill="none" width="2.989" height="0.562"/>
```

FZP declaration:
```xml
<breadboardView>
  <p svgId="connector0pin" layer="breadboard" terminalId="connector0terminal" />
</breadboardView>
```

**When to use terminalId:**
- Long pins/pads where you want wires to attach at one end, not the center
- Through-hole leads where the attachment point should be at the tip
- Most parts don't need it - default center attachment works fine

**Summary:**
- **connectorXpad/pin** = connector shape and area (required in SVG)
- **connectorXterminal** = wire attachment point (optional, defaults to center if omitted)

### Nested SVG Structure (Solves Inkscape Duplicate ID Problem!)

**This nested structure is for PURE THROUGH-HOLE parts only:**
```xml
<g id="copper0">
  <g id="copper1">
    <!-- All connector pads defined HERE only once -->
    <circle 
      id="connector0pad" 
      cx="5.08" 
      cy="5.08" 
      r="1.8" 
      fill="none" 
      stroke="rgb(255, 191, 0)" 
      stroke-width="1.2"/>
  </g>
</g>
```

**Why this works:**
- The shape elements are only defined once (no duplicate IDs!)
- Inkscape will not complain about duplicate IDs
- Fritzing knows to use these elements for BOTH copper0 and copper1 because copper1 is nested inside copper0
- The Fritzing Parts Editor requires this nested structure for through-hole parts

**In the FZP file, you still reference both layers:**
```xml
<pcbView>
    <p svgId="connector0pad" layer="copper0" />
    <p svgId="connector0pad" layer="copper1" />
</pcbView>
```

### SMD Parts (Surface Mount)

**According to official Fritzing documentation:**
- SMD parts use **only the `copper1` layer** in the FZP and SVG
- When an SMD part is placed on the bottom layer in Fritzing, the layer is **automatically updated to `copper0`**
- SMD pads use **solid fill** (not stroke)

**SMD SVG Example:**
```xml
<g id="copper1">
  <!-- SMD pads with solid fill -->
  <rect id="connector0pad" x="5" y="5" width="3" height="2" 
        fill="rgb(255, 191, 0)" stroke="none"/>
  <rect id="connector1pad" x="15" y="5" width="3" height="2" 
        fill="rgb(255, 191, 0)" stroke="none"/>
</g>
```

**SMD FZP Example:**
```xml
<connector id="connector0" name="PAD1">
  <views>
    <pcbView>
      <p svgId="connector0pad" layer="copper1" />
    </pcbView>
  </views>
</connector>
```

### Mixed SMD and Through-Hole Parts

**Note:** The official Fritzing documentation does not explicitly cover parts with BOTH SMD and through-hole connectors. For such cases, you may need to examine existing Fritzing parts in the [fritzing-parts repository](https://github.com/fritzing/fritzing-parts) to see how they are structured, or ask in the [Fritzing forum](https://forum.fritzing.org/).

**Summary from Official Documentation:**
- **Pure through-hole parts**: Use nesting (copper1 inside copper0), reference same ID in both layers in FZP
- **Pure SMD parts**: Only define copper1 layer, Fritzing auto-flips to copper0 when placed on bottom
- **Mixed parts**: Not explicitly documented - check existing parts for examples

## Mounting Holes and Special Elements

### Plated Through-Holes (Component Connectors)

**For connector pads that are plated through-holes:**
- These MUST be defined in the FZP file as connectors
- Use the nested SVG structure (copper1 inside copper0)
- The FZP file references the svgId in both copper layers
- Simply having a circle in the SVG is NOT enough - it must be declared as a connector in the FZP

**Example SVG:**
```xml
<g id="copper0">
  <g id="copper1">
    <circle id="connector0pad" cx="10" cy="10" r="1.5" 
            fill="none" stroke="rgb(255, 191, 0)" stroke-width="1.2"/>
  </g>
</g>
```

**Required FZP declaration:**
```xml
<connector id="connector0" name="Pin1">
  <views>
    <pcbView>
      <p svgId="connector0pad" layer="copper0" />
      <p svgId="connector0pad" layer="copper1" />
    </pcbView>
  </views>
</connector>
```

### Vias (Routing Holes)

**Note:** Vias for routing between PCB layers are typically created by Fritzing's routing tool, not as part of custom component footprints. The official documentation does not cover how to create vias within a component part. If you need vias as part of your component design, check existing Fritzing parts or ask in the forum.

### Non-Plated Holes (Mounting Holes)

**According to official Fritzing documentation**, for mounting holes or non-plated holes:

**Use `id="nonconn..."` prefix:**
- Any `<circle>` element with an ID starting with `nonconn` is treated as a **non-plated hole**
- The hole barrel is NOT plated (no copper inside the hole)
- Can optionally have copper **pads on top and bottom surfaces** if `stroke-width` is greater than zero
- Does NOT need to be declared in the FZP file as a connector

**Example - Pure mounting hole (no copper pads):**
```xml
<g id="copper0">
  <g id="copper1">
    <circle id="nonconn1" cx="5" cy="5" r="1.6" 
            fill="none" stroke="none"/>
  </g>
</g>
```

**Example - Non-plated hole WITH copper pads on surfaces (for mechanical soldering):**
```xml
<g id="copper0">
  <g id="copper1">
    <circle id="nonconn1" cx="5" cy="5" r="1.6" 
            fill="none" stroke="rgb(255, 191, 0)" stroke-width="1.0"/>
  </g>
</g>
```

**Important:** `nonconn` holes are **NON-PLATED** - the hole barrel has no copper plating.

### Mechanical Anchor Holes (Plated Through for Soldering)

**For holes like XT30 mechanical anchors** that need to be **plated through the barrel** for mechanical strength:

**You MUST define them as connectors in the FZP file:**
- Plated through-holes can ONLY be created by declaring them as connectors
- The `nonconn` prefix explicitly creates non-plated holes
- Even if not electrically significant, declare it as a connector

**SVG Example:**
```xml
<g id="copper0">
  <g id="copper1">
    <circle id="connector2pad" cx="20" cy="10" r="1.5" 
            fill="none" stroke="rgb(255, 191, 0)" stroke-width="1.2"/>
  </g>
</g>
```

**FZP Declaration (Required for plating):**
```xml
<connector id="connector2" name="Mechanical Anchor">
  <description>Mechanical anchor hole (not electrically connected)</description>
  <views>
    <pcbView>
      <p svgId="connector2pad" layer="copper0" />
      <p svgId="connector2pad" layer="copper1" />
    </pcbView>
  </views>
</connector>
```

**Summary:**
- **Non-plated holes**: Use `nonconn` prefix (no FZP declaration needed)
- **Plated through-holes**: MUST be declared as connectors in FZP file (even if not electrically used)

### SMD Pads (No Drill Hole)

**For circular SMD pads** that should NOT have a drill hole:

**Use `drill="no"` attribute:**
- Normally, the gerber exporter treats `<circle>` elements in copper layers as drill locations
- To create a circular SMD pad without a hole, add `drill="no"`

**Example:**
```xml
<g id="copper1">
  <circle id="connector0pad" cx="10" cy="10" r="2" 
          drill="no" 
          fill="rgb(255, 191, 0)" stroke="none"/>
</g>
```

**Summary:**
- **Vias/plated holes**: Normal through-hole structure (nested, stroke, no special attributes)
- **Non-plated mounting holes**: ID starts with `nonconn`
- **Circular SMD pads**: Add `drill="no"` attribute

### Complete SVG Template for Through-Hole (Correct Nesting!)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg version="1.2" xmlns="http://www.w3.org/2000/svg" 
     width="0.1in" height="0.1in" viewBox="0 0 7.2 7.2">
  
  <!-- Copper layers - NESTED structure -->
  <g id="copper0">
    <g id="copper1">
      <!-- Pads defined only ONCE inside nested group -->
      <circle id="connector0pad" cx="3.6" cy="3.6" r="1.8" 
              fill="none" stroke="rgb(255, 191, 0)" stroke-width="1.2"/>
    </g>
  </g>
  
  <!-- Silkscreen Layer -->
  <g id="silkscreen">
    <rect x="0.5" y="0.5" width="6.2" height="6.2" 
          fill="none" stroke="white" stroke-width="0.2"/>
    <text x="3.6" y="8" font-family="DroidSans" font-size="1.5" 
          text-anchor="middle" fill="white">P1</text>
  </g>
  
</svg>
```

## Best Practices

### Connector IDs
- **Through-hole pads**: Use the SAME ID in both copper0 and copper1 layers (via nesting)
- **PCB View**: `connector0pad`, `connector1pad`, `connector2pad`, etc. (defines pad shape/area)
- **Breadboard View**: `connector0pin` (connector area), optionally `connector0terminal` (wire attachment point)
- **Schematic View**: `connector0pin` (connector area), optionally `connector0terminal` (wire attachment point)
- The connector numbers must match the connector definitions in the FZP file
- **terminalId is optional** - if omitted, wires attach at the center of the connector area

### Dimensions
- Use **millimeters** as the base unit or **inches** with proper conversion
- Standard hole sizes: 0.8mm - 1.0mm diameter
- Pad size: typically 1.6mm - 2.0mm radius for the annular ring

### Stroke vs Fill
- **Through-hole pads**: Use `stroke` (not fill) for annular rings
- Stroke width defines the copper ring around the hole
- `fill="none"` ensures proper hole detection

### Colors for Fritzing PCB View

#### Standard Fritzing PCB Colors (for Inkscape)

| Layer | Color Name | RGB | Hex | Usage |
|-------|-----------|-----|-----|-------|
| **copper0** (bottom/solder side) | Gold/Orange | `rgb(255, 191, 0)` | `#FFBF00` | Copper pads, traces, fills |
| **copper1** (top/component side) | Gold/Orange | `rgb(255, 191, 0)` | `#FFBF00` | Copper pads, traces, fills |
| **Silkscreen** | White | `rgb(255, 255, 255)` | `#FFFFFF` | Component outlines, labels, reference designators |

**Important:** Both copper0 and copper1 use the **same color** (`#FFBF00`) because they represent the same copper material on different sides of the PCB. The layer name (copper0 vs copper1) determines which side, not the color.

**How Fritzing Displays Layers:**
- In your **SVG file**, both copper0 and copper1 should use the same color: `#FFBF00`
- In **Fritzing's interface**, the software may display them differently for visualization:
  - You can toggle between top view and bottom view
  - Fritzing may shade or dim one layer when viewing the other
  - The rendering engine handles visual separation for clarity
- The color you define in SVG is for **authoring**, Fritzing's display is for **viewing**

**Design Tip: Using Different Colors in Inkscape**
- **During design**: You CAN use different colors for copper0 and copper1 in Inkscape to make them easier to distinguish
  - Example: copper1 = `#FFBF00` (orange), copper0 = `#FF8800` (darker orange)
  - Example: copper1 = `#FFBF00` (orange), copper0 = `#0099FF` (blue)
- **Before exporting**: Change both layers to the standard `#FFBF00` for consistency
- **Alternative**: Keep different colors if you prefer - Fritzing will display exactly what's in your SVG
  - No technical problems, but may look non-standard compared to other Fritzing parts
  - Helpful if you want visual distinction in the PCB view for complex layouts

**Recommendation:** Use different colors while designing for clarity, then standardize to `#FFBF00` for both layers in the final version.

#### Alternative Copper Colors
- **Copper ENIG** (modern finish): `rgb(205, 175, 149)` / `#CDAF95` (lighter, silvery)
- **Copper HASL** (traditional): `rgb(255, 191, 0)` / `#FFBF00` (gold/orange) - **Recommended**

#### Inkscape Settings for PCB Design
- **Stroke width for pads**: 1.0mm - 1.5mm typical
- **Stroke for traces**: 0.4mm - 1.0mm depending on current requirements
- **Silkscreen line width**: 0.15mm - 0.25mm (0.2mm recommended)
- **Text size for silkscreen**: 1.0mm - 1.5mm height minimum

#### Important Notes
- Always use **fill="none"** for through-hole pads with stroke only
- Use **solid fills** for SMD pads (no stroke)
- Silkscreen should contrast with the PCB substrate (white on green)

## Multi-Pin Component Example
```xml
<g id="copper1">
  <circle id="connector0pad" c (Nested Structure)
```xml
<g id="copper0">
  <g id="copper1">
    <!-- All pads defined once inside nested groups -->
    <circle id="connector0pad" cx="5.08" cy="5.08" r="1.8" 
            fill="none" stroke="rgb(255, 191, 0)" stroke-width="1.2"/>
    <circle id="connector1pad" cx="10.16" cy="5.08" r="1.8" 
            fill="none" stroke="rgb(255, 191, 0)" stroke-width="1.2"/>
    <circle id="connector2pad" cx="15.24" cy="5.08" r="1.8" 
            fill="none" stroke="rgb(255, 191, 0)" stroke-width="1.2"/>
  </g>
</g>
```

**Critical:** copper1 is NESTED inside copper0. All connector shapes are defined only once, eliminating duplicate ID errors in Inkscape!
1. **Different IDs for through-holes** - copper0 and copper1 MUST use the SAME ID for through-hole pads (e.g., both use `connector0pad`)
2. **Using fill instead of stroke** - Through-hole pads need stroke with fill="none"
3. **Wrong units** - Always specify units clearly (mm, in)
4. **Missing viewBox** - Essential for proper scaling
5. **Inconsistent naming** - Keep systematic naming: `connector0pad`, `connector1pad`, etc.

## StNot nesting copper layers** - For through-hole parts, copper1 MUST be nested inside copper0 in the SVG (Fritzing Parts Editor requires this!)
2. **Defining pads separately in each layer** - This creates duplicate IDs that Inkscape will reject
3. **Using fill instead of stroke** - Through-hole pads need stroke with fill="none"
4. **Wrong units** - Always specify units clearly (mm, in)
5. **Missing viewBox** - Essential for proper scaling
## References
- Fritzing Part File Format: https://github.com/fritzing/fritzing-app/wiki
- SVG Specification: https://www.w3.org/TR/SVG/
