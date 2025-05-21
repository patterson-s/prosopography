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
    
    # File uploader
    uploaded_file = st.file_uploader("Upload career trajectory JSON file", type=["json"])
    
    if uploaded_file is not None:
        try:
            # Process uploaded file
            data = process_uploaded_file(uploaded_file)
            
            # If data is valid, show person selector
            if data:
                # Extract person name from data
                person_name = data["person"]["name"]
                
                # Person selector (dropdown)
                selected_person = st.selectbox(
                    "Select person to visualize",
                    [person_name]
                )
                
                # Show visualization for selected person
                if selected_person:
                    display_visualizations(data)
            
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
                    display_visualizations(example_data)
                else:
                    st.error("Example data is not in the correct format.")


def process_uploaded_file(uploaded_file) -> Dict[str, Any]:
    """Process the uploaded JSON file."""
    try:
        # Save uploaded file to a temporary file
        with open("temp_upload.json", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load and validate the data
        data = dp.load_json_file("temp_upload.json")
        
        if not dp.validate_career_data(data):
            st.error("The uploaded file does not have the correct structure.")
            return None
        
        return data
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None
    
    finally:
        # Clean up temporary file
        if os.path.exists("temp_upload.json"):
            os.remove("temp_upload.json")


def display_visualizations(data: Dict[str, Any]):
    """Display visualizations for the provided data."""
    # Prepare timeline data
    df_sorted, metatype_to_y = dp.prepare_timeline_data(data)
    
    if len(df_sorted) < 2:
        st.warning("Insufficient data points for visualization. Need at least 2 career events.")
        return
    
    # Create sidebar for filtering options
    st.sidebar.header("Filter Options")
    
    # Filter by metatype
    available_metatypes = sorted(df_sorted["metatype"].unique())
    selected_metatypes = st.sidebar.multiselect(
        "Filter by career type",
        options=available_metatypes,
        default=available_metatypes
    )
    
    # Apply filters
    if selected_metatypes:
        filtered_df = df_sorted[df_sorted["metatype"].isin(selected_metatypes)]
    else:
        filtered_df = df_sorted
    
    if len(filtered_df) < 1:
        st.warning("No data points match the selected filters.")
        return
    
    # Create and display career timeline visualization
    st.subheader(f"Career Timeline: {data['person']['name']}")
    
    # Create a clean visualization with the filtered data
    fig, _ = viz.plot_career_timeline(filtered_df, metatype_to_y)
    st.pyplot(fig)
    
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
    display_df = filtered_df[["metatype", "organization", "role", "timeline_date", "start_date", "end_date"]].copy()
    display_df["year"] = display_df["timeline_date"].astype(int)
    
    # Calculate duration for each role
    def calculate_duration(row):
        start = row["start_date"] if row["start_date"] else row["timeline_date"]
        end = row["end_date"] if row["end_date"] else row["timeline_date"]
        
        try:
            start = float(start)
            end = float(end)
            return max(end - start, 1)  # Minimum duration of 1 year for events with same start/end
        except (ValueError, TypeError):
            return 1  # Default to 1 year if calculation fails
    
    display_df["duration"] = display_df.apply(calculate_duration, axis=1)
    display_df["duration"] = display_df["duration"].round(1)
    
    # Sort by year
    display_df = display_df.sort_values("year")
    
    # Display the table with better column names
    st.dataframe(
        display_df[["year", "metatype", "role", "organization", "duration"]].rename(
            columns={
                "year": "Year",
                "metatype": "Type",
                "role": "Role",
                "organization": "Organization",
                "duration": "Duration (Years)"
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
    main()