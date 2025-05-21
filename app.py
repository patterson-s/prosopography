import streamlit as st
import os
import pandas as pd
from typing import List, Dict, Any

import data_processing as dp
import visualization as viz

# Set page configuration
st.set_page_config(
    page_title="Career Trajectory Visualization",
    page_icon="📊",
    layout="wide"
)

def main():
    """Main function to run the Streamlit app."""
    # Set title
    st.title("Career Trajectory Visualization")
    
    # Initialize session state for storing dataset
    if 'dataset' not in st.session_state:
        st.session_state.dataset = None
    if 'temp_file_path' not in st.session_state:
        st.session_state.temp_file_path = None
    
    # Hide sidebar hamburger menu and footer
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload career trajectory JSON file", type=["json"])
    
    if uploaded_file is not None:
        try:
            # Process uploaded file
            process_uploaded_file(uploaded_file)
            
            # If data is loaded, extract person names
            if st.session_state.dataset is not None:
                person_names = dp._extract_names_from_data(st.session_state.dataset)
                
                if not person_names:
                    st.error("No valid person data found in the uploaded file.")
                else:
                    # Person selector (dropdown)
                    selected_person = st.selectbox(
                        "Select person to visualize",
                        person_names
                    )
                    
                    # Get data for selected person
                    if selected_person:
                        person_data = dp.get_person_data(st.session_state.dataset, selected_person)
                        
                        if person_data and dp.validate_career_data(person_data):
                            display_visualizations(person_data)
                        else:
                            st.error(f"Invalid or missing data for {selected_person}")
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        # Show instructions when no file is uploaded
        st.info("Please upload a JSON file with career trajectory data.")
        
        # Example file link for testing
        if os.path.exists("data/anand_panyarachun_career_subset.json"):
            if st.button("Use example data"):
                example_data = dp.load_json_file("data/anand_panyarachun_career_subset.json")
                if dp.validate_career_data(example_data):
                    st.session_state.dataset = example_data
                    display_visualizations(example_data)
                else:
                    st.error("Example data is not in the correct format.")


def process_uploaded_file(uploaded_file) -> None:
    """Process the uploaded JSON file and store in session state."""
    try:
        # Save uploaded file to a temporary file
        temp_file_path = "temp_upload.json"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Store the temp file path in session state
        st.session_state.temp_file_path = temp_file_path
        
        # Load the data
        data = dp.load_json_file(temp_file_path)
        
        # Store the dataset in session state
        st.session_state.dataset = data
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise e


def cleanup_temp_file():
    """Clean up temporary file."""
    if st.session_state.temp_file_path and os.path.exists(st.session_state.temp_file_path):
        os.remove(st.session_state.temp_file_path)
        st.session_state.temp_file_path = None


def display_visualizations(data: Dict[str, Any]):
    """Display visualizations for the provided data."""
    # Prepare timeline data
    df_sorted, metatype_to_y = dp.prepare_timeline_data(data)
    
    if len(df_sorted) < 2:
        st.warning("Insufficient data points for visualization. Need at least 2 career events.")
        return
    
    # No filtering - always use the full dataset
    filtered_df = df_sorted
    
    # Create and display career timeline visualization
    st.subheader(f"Career Timeline: {data['person']['name']}")
    
    # Create a clean interactive visualization with the filtered data
    fig = viz.plot_career_timeline_plotly(filtered_df, metatype_to_y)
    st.plotly_chart(fig, use_container_width=True)
    
    # Find longest role
    longest_role, longest_duration = viz.find_longest_role(filtered_df)
    
    # Display key career insights
    st.subheader("Key Career Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display career statistics
        st.markdown("**Career Timeline Statistics**")
        
        # Calculate statistics
        event_count = len(filtered_df)
        career_span = filtered_df["timeline_date"].max() - filtered_df["timeline_date"].min()
        metatype_counts = filtered_df["metatype"].value_counts()
        
        # Display metrics
        st.metric("Total Career Events", event_count)
        st.metric("Career Span (Years)", f"{career_span:.1f}")
        st.metric("Most Common Type", metatype_counts.index[0] if not metatype_counts.empty else "N/A")
        
        # Display longest role information
        if longest_role and longest_duration > 0:
            st.markdown("**Longest Role**")
            st.markdown(f"**{longest_role.get('role', 'Unknown Role')}** at **{longest_role.get('organization', 'Unknown Organization')}**")
            
            # Check if it's an open-ended position
            if 'is_open_ended' in longest_role and longest_role['is_open_ended']:
                st.markdown(f"**Duration:** Ongoing/No End Date (showing as {longest_duration:.1f} years)")
            else:
                st.markdown(f"**Duration:** {longest_duration:.1f} years")
                
            st.markdown(f"**Type:** {longest_role.get('metatype', 'Unknown')}")
    
    with col2:
        # Display year-based distribution
        st.markdown("**Distribution by Years in Each Type**")
        fig, _ = viz.plot_metatype_distribution_by_years(filtered_df)
        st.pyplot(fig)
    
    # Display interactive table of career events
    st.subheader("Career Events")
    
    # Create a clean table for display
    display_df = filtered_df.copy()
    display_df["year"] = display_df["timeline_date"].astype(int)
    
    # Calculate duration for each role
    def calculate_duration(row):
        # First check if this is an open-ended position
        if "is_open_ended" in row and row["is_open_ended"]:
            return "Ongoing/No End Date"
            
        # Use numeric_start and numeric_end if available (from the updated prepare_timeline_data)
        if "numeric_start" in row and "numeric_end" in row:
            duration = row["numeric_end"] - row["numeric_start"]
            return f"{duration:.1f}"
        
        # Otherwise, fall back to original calculation
        start = row["start_date"] if row["start_date"] else row["timeline_date"]
        end = row["end_date"] if row["end_date"] else row["timeline_date"]
        
        try:
            start = float(start)
            end = float(end)
            duration = max(end - start, 1)  # Minimum duration of 1 year for events with same start/end
            return f"{duration:.1f}"
        except (ValueError, TypeError):
            return "1.0"  # Default to 1 year if calculation fails
    
    display_df["duration"] = display_df.apply(calculate_duration, axis=1)
    
    # Add status column to indicate open-ended positions
    display_df["status"] = "Completed"
    if "is_open_ended" in filtered_df.columns:
        display_df["status"] = filtered_df["is_open_ended"].apply(
            lambda x: "Ongoing/No End Date" if x else "Completed")
    
    # Sort by year
    display_df = display_df.sort_values("year")
    
    # Display the table with better column names
    display_columns = ["year", "metatype", "role", "organization", "duration", "status"]
    
    st.dataframe(
        display_df[display_columns].rename(
            columns={
                "year": "Year",
                "metatype": "Type",
                "role": "Role",
                "organization": "Organization",
                "duration": "Duration (Years)",
                "status": "Status"
            }
        ),
        use_container_width=True
    )
    
    # Show distribution by event count in expandable section
    with st.expander("View Distribution by Event Count"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create and display metatype distribution
            st.markdown("**Distribution by Number of Events**")
            fig, _ = viz.plot_metatype_distribution(filtered_df)
            st.pyplot(fig)
        
        with col2:
            # Display metatype counts as a table
            st.markdown("**Event Counts by Type**")
            metatype_counts = filtered_df["metatype"].value_counts().reset_index()
            metatype_counts.columns = ["Type", "Count"]
            st.dataframe(metatype_counts, use_container_width=True)
    
    # Display raw data table
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_temp_file()