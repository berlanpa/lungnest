# Lung Viewer - DICOM PACS Viewer

A specialized DICOM viewer for lung imaging analysis, built on the DWV (DICOM Web Viewer) framework.

## Features

- **DICOM Image Viewing**: Load and display medical lung imaging data
- **Multi-slice Navigation**: Browse through volumetric lung CT scans
- **Window/Level Adjustment**: Optimize image contrast for lung tissue analysis
- **Measurement Tools**: Built-in tools for medical measurements
- **Segmentation Support**: Advanced segmentation capabilities for lung analysis
- **Modern UI**: Clean, responsive interface optimized for medical imaging

## Quick Start

### Development

```bash
# Install dependencies
yarn install

# Build the application
yarn build

# Development build with watch mode
yarn dev
```

### Deployment

The application is configured for deployment on Vercel:

```bash
# Deploy to Vercel
vercel
```

## Project Structure

```
lung-viewer/
├── src/                    # DWV library source code
├── tests/pacs/            # PACS viewer application
│   ├── index.html         # Main HTML file
│   ├── viewer.js          # Main application logic
│   └── viewer.ui.*.js     # UI components
├── tests/data/SE1/        # Sample lung DICOM data
├── config/                # Build configuration
├── package.json           # Dependencies and scripts
└── vercel.json           # Deployment configuration
```

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Medical Imaging**: DWV (DICOM Web Viewer) library
- **Graphics**: Konva.js for 2D canvas manipulation
- **Build Tool**: Webpack
- **Deployment**: Vercel

## License

GPL-3.0 License - see the original DWV project for full license details.
