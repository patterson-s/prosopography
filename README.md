# Career Trajectory Visualization Dashboard

A Streamlit application for visualizing career trajectories using prosopographical data.

## Overview

This dashboard allows users to upload JSON files containing career trajectory data and visualize them as timeline plots. It shows the progression of a person's career across different types of roles, organizations, and time periods.

## Features

- Upload JSON files with career event data
- Select a person to visualize from the uploaded data
- View career trajectory timeline visualization
- See distribution of career events by type
- Examine raw data in tabular format

## Getting Started

### Prerequisites

- Python 3.7+
- Required packages (install with `pip install -r requirements.txt`):
  - streamlit
  - pandas
  - matplotlib
  - numpy

### Running the Application

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Data Format

The application expects JSON files with the following structure:

```json
{
  "person": {
    "name": "Person Name",
    "metadata": { ... }
  },
  "career_events": [
    {
      "metatype": "category",
      "organization": "Organization Name",
      "role": "Role Title",
      "start_date": "YYYY",
      "end_date": "YYYY",
      ...
    },
    ...
  ]
}
```

## Project Structure

- `app.py`: Main Streamlit application
- `data_processing.py`: Data loading, validation, and preparation
- `visualization.py`: Timeline plotting logic
- `utils/helpers.py`: Utility functions
- `data/`: Sample data files

## Future Development

This is an initial version focused on core visualization functionality. Future versions will add:

- Support for multiple people in a single dataset
- Additional visualization types
- Advanced filtering and comparison options
- Enhanced user interface