import json
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON data from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file format")
    except Exception as e:
        raise IOError(f"Error reading file: {str(e)}")


def validate_career_data(data: Dict[str, Any]) -> bool:
    """Validate if data has expected structure for career visualization."""
    try:
        # Check if data contains necessary keys
        if "person" not in data or "career_events" not in data:
            return False
        
        # Check person data format
        if "name" not in data["person"]:
            return False
        
        # Check if career_events is a list with at least one event
        if not isinstance(data["career_events"], list) or len(data["career_events"]) == 0:
            return False
        
        # Check if first career event has expected keys
        first_event = data["career_events"][0]
        required_keys = ["metatype", "organization", "role", "start_date", "end_date"]
        
        if not all(key in first_event for key in required_keys):
            return False
            
        return True
    except Exception:
        return False


def extract_person_names(data_list: List[Dict[str, Any]]) -> List[str]:
    """Extract list of person names from a list of career datasets."""
    names = []
    for data in data_list:
        if validate_career_data(data) and "person" in data and "name" in data["person"]:
            names.append(data["person"]["name"])
    return names


def prepare_timeline_data(data: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Convert career events JSON to DataFrame format for timeline visualization."""
    events = data["career_events"]
    
    # Process the events into a list of dictionaries
    processed_events = []
    
    for event in events:
        # Skip events without dates
        if not event["start_date"] and not event["end_date"]:
            continue
            
        # Use the earliest date available for timeline
        timeline_date = event["start_date"] if event["start_date"] else event["end_date"]
        
        # Try to convert timeline_date to numeric
        try:
            timeline_date = float(timeline_date)
        except ValueError:
            # Skip events with non-numeric dates
            continue
            
        processed_events.append({
            "metatype": event["metatype"],
            "organization": event["organization"],
            "role": event["role"],
            "timeline_date": timeline_date,
            "start_date": event["start_date"],
            "end_date": event["end_date"]
        })
    
    # Create DataFrame
    df = pd.DataFrame(processed_events)
    
    # Map metatypes to y-positions
    unique_metatypes = sorted(df["metatype"].unique())
    metatype_to_y = {metatype: i for i, metatype in enumerate(unique_metatypes)}
    
    # Add y-position column
    df["y_pos"] = df["metatype"].map(metatype_to_y)
    
    # Sort by timeline date
    df_sorted = df.sort_values(by="timeline_date").reset_index(drop=True)
    
    return df_sorted, metatype_to_y


def get_person_data(data: Dict[str, Any], person_name: str) -> Optional[Dict[str, Any]]:
    """Get data for a specific person from the full dataset."""
    if data["person"]["name"] == person_name:
        return data
    return None