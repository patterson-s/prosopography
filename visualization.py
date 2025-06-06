import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List, Any, Optional
import io
from matplotlib.figure import Figure
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def create_color_mapping(metatypes: List[str]) -> Dict[str, str]:
    """Create a mapping of metatypes to colors."""
    # Define a better color palette with more distinct colors
    colors = [
        '#1f77b4',  # blue
        '#ff7f0e',  # orange
        '#2ca02c',  # green
        '#d62728',  # red
        '#9467bd',  # purple
        '#8c564b',  # brown
        '#e377c2',  # pink
        '#7f7f7f',  # gray
        '#bcbd22',  # olive
        '#17becf'   # teal
    ]
    
    # Map metatypes to colors
    color_map = {}
    for i, metatype in enumerate(sorted(metatypes)):
        color_map[metatype] = colors[i % len(colors)]
        
    return color_map


def prepare_visualization_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare dataframe for visualization by adding sub-indices for overlapping events."""
    df_sorted = df.copy()
    
    # Create a mapping of metatypes to colors
    metatypes = df_sorted["metatype"].unique()
    color_map = create_color_mapping(metatypes)
    df_sorted["color"] = df_sorted["metatype"].map(color_map)
    
    # Initialize sub_index column
    df_sorted["sub_index"] = 0
    
    # For each metatype-year combo, assign a sub-index to spread them out slightly
    year_precision = 0.2  # Controls vertical spread within same metatype
    
    meta_year_tracker = {}
    for idx, row in df_sorted.iterrows():
        year_key = (row["metatype"], int(row["timeline_date"]))
        if year_key not in meta_year_tracker:
            meta_year_tracker[year_key] = 0
        else:
            meta_year_tracker[year_key] += 1
        df_sorted.at[idx, "sub_index"] = meta_year_tracker[year_key]
    
    # Adjust y position by sub_index offset
    df_sorted["y_adjusted"] = df_sorted["y_pos"] + df_sorted["sub_index"] * year_precision
    
    return df_sorted


def plot_career_timeline_plotly(df: pd.DataFrame, metatype_to_y: Dict[str, float], person_data: Dict[str, Any] = None):
    """Create an interactive career timeline visualization with hover information using Plotly."""
    # Prepare data with adjusted positions for overlapping events
    df_sorted = prepare_visualization_data(df)
    
    # Create figure
    fig = go.Figure()
    
    # Get a color map for all metatypes
    unique_metatypes = df_sorted["metatype"].unique()
    color_map = create_color_mapping(unique_metatypes)
    
    # Create a mapping of metatypes to their index (for y-axis positioning)
    metatype_indices = {mt: i for i, mt in enumerate(sorted(unique_metatypes))}
    
    # Add position duration lines
    for i, row in df_sorted.iterrows():
        if 'numeric_start' in row and 'numeric_end' in row:
            # Determine line style based on whether position is open-ended
            is_open_ended = 'is_open_ended' in row and row['is_open_ended']
            dash = 'dash' if is_open_ended else None
            
            # Create hover text
            hover_text = f"<b>{row['role']}</b><br>" + \
                         f"<b>Organization:</b> {row['organization']}<br>" + \
                         f"<b>Type:</b> {row['metatype'].capitalize()}<br>"
            
            if is_open_ended:
                hover_text += "<b>Duration:</b> Ongoing/No End Date"
            else:
                duration = row['numeric_end'] - row['numeric_start']
                hover_text += f"<b>Duration:</b> {duration:.1f} years"
            
            # Add line for position duration
            fig.add_trace(go.Scatter(
                x=[row['numeric_start'], row['numeric_end']],
                y=[row['y_adjusted'], row['y_adjusted']],
                mode='lines',
                line=dict(color=row['color'], width=4, dash=dash),
                showlegend=False,
                hoverinfo='none'
            ))
            
            # Add marker for position start
            fig.add_trace(go.Scatter(
                x=[row['timeline_date']],
                y=[row['y_adjusted']],
                mode='markers',
                marker=dict(
                    color=row['color'],
                    size=12,
                    line=dict(color='black', width=1)
                ),
                name=row['metatype'].capitalize(),
                text=hover_text,
                hoverinfo='text',
                hoverlabel=dict(bgcolor='white', font_size=12),
                showlegend=False
            ))
    
    # Add HLP year vertical line if available
    if person_data and 'person' in person_data and 'metadata' in person_data['person']:
        hlp_year = person_data['person']['metadata'].get('hlp_year')
        hlp_name = person_data['person']['metadata'].get('hlp', 'High-Level Panel')
        
        if hlp_year:
            try:
                hlp_year_numeric = float(hlp_year)
                
                # Add vertical line for HLP year
                fig.add_vline(
                    x=hlp_year_numeric,
                    line=dict(
                        color='red',
                        width=3,
                        dash='dot'
                    ),
                    annotation_text=f"HLP: {hlp_year}",
                    annotation_position="top",
                    annotation=dict(
                        font=dict(size=12, color='red'),
                        bgcolor='white',
                        bordercolor='red',
                        borderwidth=1
                    )
                )
                
                # Add HLP year to legend
                fig.add_trace(go.Scatter(
                    x=[None],
                    y=[None],
                    mode='lines',
                    line=dict(color='red', width=3, dash='dot'),
                    name=f'HLP Year ({hlp_year})',
                    showlegend=True
                ))
                
            except (ValueError, TypeError):
                # Skip if hlp_year cannot be converted to numeric
                pass
    
    # Add legend traces for metatypes
    for metatype in sorted(unique_metatypes):
        color = color_map.get(metatype, '#7f7f7f')
        
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(
                color=color,
                size=10,
                line=dict(color='black', width=1)
            ),
            name=metatype.capitalize(),
            showlegend=True
        ))
    
    # Add legend for line styles
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='black', width=3),
        name='Completed Position',
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='black', width=3, dash='dash'),
        name='Ongoing/No End Date',
        showlegend=True
    ))
    
    # Set y-axis ticks and labels
    ytick_locs = list(metatype_to_y.values())
    ytick_labels = [label.capitalize() for label in metatype_to_y.keys()]
    
    # Calculate min and max x values with some padding
    x_min = df_sorted["timeline_date"].min() - 1
    x_max = max(df_sorted["timeline_date"].max() + 1, 
                df_sorted["numeric_end"].max() + 1 if "numeric_end" in df_sorted else 0)
    
    # Update layout
    fig.update_layout(
        title='Career Trajectory Timeline',
        xaxis=dict(
            title='Year',
            gridcolor='lightgrey',
            range=[x_min, x_max],
            zeroline=False
        ),
        yaxis=dict(
            title='',
            tickvals=ytick_locs,
            ticktext=ytick_labels,
            gridcolor='#f0f0f0',
            zeroline=False
        ),
        plot_bgcolor='#f8f9fa',
        hovermode='closest',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        )
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    
    return fig


def plot_career_timeline_matplotlib(df: pd.DataFrame, metatype_to_y: Dict[str, float]):
    """Create a career timeline visualization showing trajectory between different roles."""
    # Prepare data with adjusted positions for overlapping events
    df_sorted = prepare_visualization_data(df)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create lists to populate the legend
    legend_elements = []
    
    # Draw duration lines for each position
    completed_added = False
    ongoing_added = False
    
    for i, row in df_sorted.iterrows():
        if 'numeric_start' in row and 'numeric_end' in row:
            # Determine line style based on whether position is open-ended
            is_open_ended = 'is_open_ended' in row and row['is_open_ended']
            linestyle = 'dashed' if is_open_ended else 'solid'
            
            # Draw horizontal line indicating position duration
            line = ax.plot(
                [row['numeric_start'], row['numeric_end']], 
                [row['y_adjusted'], row['y_adjusted']], 
                color=row['color'], 
                linewidth=3, 
                alpha=0.8,
                linestyle=linestyle,
                zorder=3
            )[0]
            
            # Add to legend only once for each type
            if is_open_ended and not ongoing_added:
                legend_elements.append(
                    plt.Line2D([0], [0], color='black', lw=2, linestyle='dashed', 
                               label='Ongoing/No End Date')
                )
                ongoing_added = True
            elif not is_open_ended and not completed_added:
                legend_elements.append(
                    plt.Line2D([0], [0], color='black', lw=2, 
                               label='Completed Position')
                )
                completed_added = True
    
    # Plot dots for each event (after lines so they appear on top)
    scatter = ax.scatter(
        df_sorted["timeline_date"], 
        df_sorted["y_adjusted"], 
        color=df_sorted["color"], 
        s=80,
        alpha=0.9,
        edgecolors='black',
        linewidths=1,
        zorder=10  # Ensure dots are on top
    )
    
    # Add metatype colors to legend
    all_metatypes = list(metatype_to_y.keys())
    metatypes_used = df_sorted["metatype"].unique()
    color_map = create_color_mapping(metatypes_used)
    
    for metatype in sorted(all_metatypes):
        color = color_map.get(metatype, color_map.get('other', '#7f7f7f'))
        legend_elements.append(
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                      markeredgecolor='black', markersize=8, label=metatype.capitalize())
        )
    
    # Format y-ticks to align with base metatype labels - fixed method
    ytick_locs = list(metatype_to_y.values())
    ytick_labels = list(metatype_to_y.keys())
    
    # Set the ticks and then manually set the labels (compatible with newer matplotlib)
    ax.set_yticks(ytick_locs)
    ax.set_yticklabels([label.capitalize() for label in ytick_labels])
    
    # Set labels and title
    ax.set_xlabel("Year")
    ax.set_title("Career Trajectory Timeline")
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add a light background grid for better readability
    ax.grid(axis='y', linestyle=':', alpha=0.3)
    
    # Set the x-axis range with some padding
    x_min = df_sorted["timeline_date"].min() - 1
    x_max = max(df_sorted["timeline_date"].max() + 1, 
                df_sorted["numeric_end"].max() + 1 if "numeric_end" in df_sorted else 0)
    ax.set_xlim(x_min, x_max)
    
    # Clean up y-axis appearance - fixed method
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    
    # Add a light background
    ax.set_facecolor('#f8f9fa')
    
    # Add legend at the top
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.15),
              ncol=min(5, len(legend_elements)), frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()
    
    # Convert plot to image bytes
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    
    return fig, buf.getvalue()

def plot_metatype_distribution(df: pd.DataFrame) -> Tuple[Figure, bytes]:
    """Create a visualization showing distribution of career events by metatype."""
    metatype_counts = df["metatype"].value_counts()
    
    # Prepare color mapping
    color_map = create_color_mapping(metatype_counts.index)
    colors = [color_map[metatype] for metatype in metatype_counts.index]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = metatype_counts.plot(kind='bar', ax=ax, color=colors)
    
    # Add data labels on top of bars
    for bar in bars.patches:
        ax.annotate(
            f"{int(bar.get_height())}",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    ax.set_title("Distribution of Career Events by Type")
    ax.set_xlabel("Career Type")
    ax.set_ylabel("Number of Events")
    
    # Clean up appearance
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # Convert plot to image bytes
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    
    return fig, buf.getvalue()


def plot_metatype_distribution_by_years(df: pd.DataFrame) -> Tuple[Figure, bytes]:
    """Create a pie chart showing distribution of career events by metatype based on years spent."""
    # Create a copy of the dataframe to work with
    df_copy = df.copy()
    
    # Calculate duration of each event
    def calculate_duration(row):
        start = row["start_date"] if row["start_date"] else row["timeline_date"]
        end = row["end_date"] if row["end_date"] else row["timeline_date"]
        
        try:
            start = float(start)
            end = float(end)
            return max(end - start, 1)  # Minimum duration of 1 year for events with same start/end
        except (ValueError, TypeError):
            return 1  # Default to 1 year if calculation fails
    
    df_copy["duration"] = df_copy.apply(calculate_duration, axis=1)
    
    # Group by metatype and sum durations
    years_by_metatype = df_copy.groupby("metatype")["duration"].sum()
    
    # Prepare color mapping
    color_map = create_color_mapping(years_by_metatype.index)
    colors = [color_map[metatype] for metatype in years_by_metatype.index]
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot pie chart with percentages
    wedges, texts, autotexts = ax.pie(
        years_by_metatype, 
        labels=years_by_metatype.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'edgecolor': 'w', 'linewidth': 1}
    )
    
    # Enhance text appearance
    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
        autotext.set_color('white')
    
    # Add title and annotation
    ax.set_title("Distribution of Career by Years Spent in Each Type", fontsize=14, pad=20)
    total_years = years_by_metatype.sum()
    plt.annotate(
        f"Total: {total_years:.1f} years",
        xy=(0, 0),
        xytext=(0, -30),
        textcoords="offset points",
        ha="center",
        fontsize=12
    )
    
    plt.tight_layout()
    
    # Convert plot to image bytes
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    
    return fig, buf.getvalue()


def find_longest_role(df: pd.DataFrame) -> Tuple[Dict[str, Any], float]:
    """Find the longest role in the career data."""
    # Create a copy of the dataframe to work with
    df_copy = df.copy()
    
    # Calculate duration of each event
    def calculate_duration(row):
        start = row["start_date"] if row["start_date"] else row["timeline_date"]
        end = row["end_date"] if row["end_date"] else row["timeline_date"]
        
        try:
            start = float(start)
            end = float(end)
            return max(end - start, 1)  # Minimum duration of 1 year for events with same start/end
        except (ValueError, TypeError):
            return 1  # Default to 1 year if calculation fails
    
    df_copy["duration"] = df_copy.apply(calculate_duration, axis=1)
    
    # Find the role with maximum duration
    if len(df_copy) > 0:
        longest_idx = df_copy["duration"].idxmax()
        longest_role = df_copy.loc[longest_idx]
        return longest_role.to_dict(), longest_role["duration"]
    
    return {}, 0