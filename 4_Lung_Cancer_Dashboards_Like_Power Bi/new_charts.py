import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import Markdown as md
import os
from typing import List, Dict, Union, Optional, Any, Tuple

class BaseChart:
    """
    Base class for all chart types with common functionality.
    """
    def __init__(
        self,
        df: pd.DataFrame,
        title: str = "",
        height: int = 600,
        width: int = 900,
        x_title: str = "",
        y_title: str = "",
        color_sequence: List[str] = None,
        labels: Dict[str, str] = None,
        hover_data: Dict[str, bool] = None,
        legend_title: str = "",
        show_legend: bool = True,
        legend_font_size: int = 16,
        facet_row: str = None,
        facet_col: str = None,
        facet_col_spacing: float = 0.02,
        facet_row_spacing: float = 0.07,
        y_scale_range: List[float] = None,
        y_scale_percentage: bool = False,
        bar_gap: float = 0.1,
        bar_group_gap: float = 0.2,
        empty_x_axis: bool = False,
        x_axis_step: bool = False
    ):
        """
        Initialize the base chart with common parameters.
        
        Args:
            df: Pandas DataFrame containing the data
            title: Chart title
            height: Chart height in pixels
            width: Chart width in pixels
            x_title: X-axis title
            y_title: Y-axis title
            color_sequence: List of colors for the chart
            labels: Dictionary mapping of column names to display labels
            hover_data: Dictionary specifying which columns to show in hover data
            legend_title: Title for the legend
            show_legend: Whether to show the legend
            legend_font_size: Font size for the legend
            facet_row: Column name to create row-based facets
            facet_col: Column name to create column-based facets
            facet_col_spacing: Spacing between facet columns (0.0-0.5)
            facet_row_spacing: Spacing between facet rows (0.0-0.5)
            y_scale_range: Range for y-axis [min, max]
            y_scale_percentage: Whether to format y-axis as percentage
            bar_gap: Gap between bars (0.0-1.0)
            bar_group_gap: Gap between bar groups (0.0-1.0)
            empty_x_axis: Whether to hide x-axis ticks and labels
            x_axis_step: Whether to use integer steps for x-axis
        """
        self.df = df
        self.title = title
        self.height = height
        self.width = width
        self.x_title = x_title
        self.y_title = y_title
        self.color_sequence = color_sequence if color_sequence else px.colors.qualitative.Plotly
        self.labels = labels if labels else {}
        self.hover_data = hover_data if hover_data else {}
        self.legend_title = legend_title
        self.show_legend = show_legend
        self.legend_font_size = legend_font_size
        self.facet_row = facet_row
        self.facet_col = facet_col
        self.facet_col_spacing = facet_col_spacing
        self.facet_row_spacing = facet_row_spacing
        self.y_scale_range = y_scale_range
        self.y_scale_percentage = y_scale_percentage
        self.bar_gap = bar_gap
        self.bar_group_gap = bar_group_gap
        self.empty_x_axis = empty_x_axis
        self.x_axis_step = x_axis_step
        self.fig = None

    def update_layout(self):
        """Update the layout with common settings."""
        if self.fig is None:
            return
            
        self.fig.update_layout(
            title={
                'text': self.title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font_size=20,
            plot_bgcolor='rgba(0,0,0,0)',
            legend_title=dict(
                text=self.legend_title,
                font=dict(
                    size=self.legend_font_size,
                    family='Arial',
                    color="#008080"
                )
            ),
            showlegend=self.show_legend,
            margin=dict(t=100),
            bargap=self.bar_gap,  # Gap between bars
            bargroupgap=self.bar_group_gap  # Gap between bar groups
        )
        
        # X-axis configuration
        if self.x_axis_step:
            self.fig.update_xaxes(
                title_text=self.x_title,
                showline=True,
                linecolor='gray',
                title_font=dict(
                    size=18,
                    color="#008080"
                ),
                tickfont=dict(
                    size=12,
                    family='Arial'
                ),
                tickmode='linear',
                dtick=1
            )
        else:
            self.fig.update_xaxes(
                title_text=self.x_title,
                showline=True,
                linecolor='gray',
                title_font=dict(
                    size=18,
                    color="#008080"
                ),
                tickfont=dict(
                    size=12,
                    family='Arial'
                )
            )
            
        # Empty x-axis if requested
        if self.empty_x_axis:
            self.fig.update_layout(
                xaxis=dict(
                    tickvals=[],  # No tick values
                    ticktext=[]   # No tick labels
                )
            )
        
        # Y-axis configuration
        y_axis_config = {
            'title_text': self.y_title,
            'showline': True,
            'linecolor': 'gray',
            'title_font': dict(
                size=18,
                color="#008080"
            ),
            'tickfont': dict(
                size=12,
                family='Arial'
            )
        }
        
        # Add y-axis range if specified
        if self.y_scale_range:
            y_axis_config['range'] = self.y_scale_range
            
        # Add percentage format if requested
        if self.y_scale_percentage:
            y_axis_config['tickformat'] = '.0%'
            
        self.fig.update_yaxes(**y_axis_config)
        
        # Handle facet annotations
        if self.facet_col is not None:
            try:
                self.fig.update_layout(yaxis2_title='')
            except:
                pass
                
            for annotation in self.fig.layout.annotations:
                annotation['font'] = {'size': 16, 'color': "#008080"}
                annotation['y'] = annotation['y'] + 0.01
                
        if self.facet_row is not None:
            try:
                self.fig.update_layout(xaxis2_title='')
            except:
                pass
                
            for annotation in self.fig.layout.annotations:
                annotation['font'] = {'size': 16, 'color': "#008080"}
                annotation['x'] = annotation['x'] + 0.01
                
    def display(self, use_streamlit: bool = False, save_path: str = None, format: str = 'png'):
        """
        Display the chart in the appropriate environment.
        
        Args:
            use_streamlit: If True, display in Streamlit, otherwise in Jupyter
            save_path: Path to save the chart image (None means don't save)
            format: Image format to save (png, jpg, svg, pdf)
        """
        if self.fig is None:
            raise ValueError("Chart has not been created yet. Call create() first.")
            
        # Save chart if path is provided
        if save_path:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Add extension if not provided
            if not any(save_path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.svg', '.pdf']):
                save_path = f"{save_path}.{format}"
                
            self.fig.write_image(save_path)
            print(f"Chart saved to {save_path}")
        
        # Display chart
        if use_streamlit:
            import streamlit as st
            st.plotly_chart(self.fig, use_container_width=True)
        else:
            self.fig.show()
            
    def create(self):
        """Create the chart - to be implemented by child classes."""
        raise NotImplementedError("Subclasses must implement create()")


class BarChart(BaseChart):
    """Class for creating bar charts."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str = None,
        text: str = None,
        orientation: str = 'v',
        barmode: str = "group",
        text_percentage: Union[bool, str] = True,
        error_y: str = None,
        text_location: str = "outside",
        **kwargs
    ):
        """
        Initialize a bar chart.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color differentiation
            text: Column name for text labels
            orientation: 'v' for vertical, 'h' for horizontal bars
            barmode: Bar mode ('group', 'stack', 'relative')
            text_percentage: Format for text labels (True for %, False for raw, str for custom)
            error_y: Column name for y-error bars
            text_location: Location of text labels ('inside', 'outside', 'auto', 'none')
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.orientation = orientation
        self.barmode = barmode
        self.text_percentage = text_percentage
        self.error_y = error_y
        self.text_location = text_location
        
    def create(self):
        """Create the bar chart."""
        # Common parameters for all chart types
        chart_params = {
            'x': self.x,
            'y': self.y,
            'labels': self.labels,
            'hover_data': self.hover_data,
            'title': self.title,
            'color_discrete_sequence': self.color_sequence,
            'height': self.height,
            'width': self.width,
            'barmode': self.barmode,
            'orientation': self.orientation,
            'facet_row': self.facet_row,
            'facet_col': self.facet_col,
            'facet_col_spacing': self.facet_col_spacing,
            'facet_row_spacing': self.facet_row_spacing
        }
        
        # Add error bars if specified
        if self.error_y:
            chart_params['error_y'] = self.error_y
            
        # Add text column if specified
        if self.text:
            chart_params['text'] = self.text
        
        # Create the bar chart
        if self.color is None:
            self.fig = px.bar(
                self.df,
                **chart_params
            )
        else:
            chart_params['color'] = self.color
            self.fig = px.bar(
                self.df,
                **chart_params
            )
        
        # Update text formatting
        if self.text:
            text_params = {
                'textfont_size': 15,
                'textposition': self.text_location,
                'insidetextanchor': 'middle',
                'textangle': 0,
                'cliponaxis': False
            }
            
            if self.text_percentage is True:
                text_params['texttemplate'] = '<b>%{text}%</b>'
            elif self.text_percentage is False:
                text_params['texttemplate'] = '<b>%{text}</b>'
            elif isinstance(self.text_percentage, str):
                text_params['texttemplate'] = f'<b>%{{text}} {self.text_percentage}</b>'
                
            self.fig.update_traces(**text_params)
        
        # Update layout
        self.update_layout()
        return self


class PieChart(BaseChart):
    """Class for creating pie charts."""
    def __init__(
        self,
        df: pd.DataFrame,
        values: str,
        names: str,
        custom_data: List[str] = None,
        hole: float = 0,
        **kwargs
    ):
        """
        Initialize a pie chart.
        
        Args:
            df: DataFrame with the data
            values: Column name for values (sizes of pie slices)
            names: Column name for names (labels of pie slices)
            custom_data: List of column names for custom hover data
            hole: Size of hole in the center (0-1, 0 for pie, >0 for donut)
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.values = values
        self.names = names
        self.custom_data = custom_data
        self.hole = hole
        
    def create(self):
        """Create the pie chart."""
        self.fig = px.pie(
            self.df,
            values=self.values,
            names=self.names,
            custom_data=self.custom_data,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width,
            hole=self.hole
        )
        
        # Update trace settings
        self.fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            opacity=1,
            texttemplate='<b>%{value:.2f} %</b>' if self.values.endswith('%') else '<b>%{percent:.1%}</b>',
            textinfo='percent',
            textfont_size=16,
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
        )
        
        # Update layout
        self.update_layout()
        return self


class ScatterPlot(BaseChart):
    """Class for creating scatter plots."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str = None,
        size: str = None,
        symbol: str = None,
        trendline: str = None,
        marginal_x: str = None,
        marginal_y: str = None,
        **kwargs
    ):
        """
        Initialize a scatter plot.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color differentiation
            size: Column name for point size
            symbol: Column name for point symbol
            trendline: Type of trendline ('ols', 'lowess')
            marginal_x: Type of marginal plot on x-axis ('histogram', 'box', 'violin')
            marginal_y: Type of marginal plot on y-axis ('histogram', 'box', 'violin')
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.symbol = symbol
        self.trendline = trendline
        self.marginal_x = marginal_x
        self.marginal_y = marginal_y
        
    def create(self):
        """Create the scatter plot."""
        self.fig = px.scatter(
            self.df,
            x=self.x,
            y=self.y,
            color=self.color,
            size=self.size,
            symbol=self.symbol,
            labels=self.labels,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width,
            trendline=self.trendline,
            marginal_x=self.marginal_x,
            marginal_y=self.marginal_y
        )
        
        # Update layout
        self.update_layout()
        return self


class LinePlot(BaseChart):
    """Class for creating line plots."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str = None,
        line_dash: str = None,
        line_shape: str = 'linear',
        markers: bool = True,
        **kwargs
    ):
        """
        Initialize a line plot.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color differentiation
            line_dash: Column name for line dash pattern
            line_shape: Line shape ('linear', 'spline', 'vh', 'hv', 'vhv', 'hvh')
            markers: Whether to show markers
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.line_dash = line_dash
        self.line_shape = line_shape
        self.markers = markers
        
    def create(self):
        """Create the line plot."""
        self.fig = px.line(
            self.df,
            x=self.x,
            y=self.y,
            color=self.color,
            line_dash=self.line_dash,
            labels=self.labels,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width,
            line_shape=self.line_shape,
            markers=self.markers
        )
        
        # Update layout
        self.update_layout()
        return self


class HistogramPlot(BaseChart):
    """Class for creating histograms."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str = None,
        y: str = None,
        color: str = None,
        nbins: int = None,
        histnorm: str = None,
        cumulative: bool = False,
        **kwargs
    ):
        """
        Initialize a histogram.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis (for vertical histogram)
            y: Column name for y-axis (for horizontal histogram)
            color: Column name for color differentiation
            nbins: Number of bins
            histnorm: Histogram normalization ('percent', 'probability', 'density', 'probability density')
            cumulative: Whether to show cumulative distribution
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.nbins = nbins
        self.histnorm = histnorm
        self.cumulative = cumulative
        
    def create(self):
        """Create the histogram."""
        self.fig = px.histogram(
            self.df,
            x=self.x,
            y=self.y,
            color=self.color,
            nbins=self.nbins,
            histnorm=self.histnorm,
            cumulative=self.cumulative,
            labels=self.labels,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width
        )
        
        # Update layout
        self.update_layout()
        return self


class BoxPlot(BaseChart):
    """Class for creating box plots."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str = None,
        y: str = None,
        color: str = None,
        points: str = 'outliers',
        notched: bool = False,
        **kwargs
    ):
        """
        Initialize a box plot.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color differentiation
            points: How to show points ('all', 'outliers', 'suspectedoutliers', False)
            notched: Whether to show notched boxes
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.points = points
        self.notched = notched
        
    def create(self):
        """Create the box plot."""
        self.fig = px.box(
            self.df,
            x=self.x,
            y=self.y,
            color=self.color,
            points=self.points,
            notched=self.notched,
            labels=self.labels,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width
        )
        
        # Update layout
        self.update_layout()
        return self


class ViolinPlot(BaseChart):
    """Class for creating violin plots."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str = None,
        y: str = None,
        color: str = None,
        box: bool = True,
        points: str = 'outliers',
        **kwargs
    ):
        """
        Initialize a violin plot.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color differentiation
            box: Whether to show box plot inside violin
            points: How to show points ('all', 'outliers', 'suspectedoutliers', False)
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.box = box
        self.points = points
        
    def create(self):
        """Create the violin plot."""
        self.fig = px.violin(
            self.df,
            x=self.x,
            y=self.y,
            color=self.color,
            box=self.box,
            points=self.points,
            labels=self.labels,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width
        )
        
        # Update layout
        self.update_layout()
        return self


class HeatmapPlot(BaseChart):
    """Class for creating heatmaps."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str = None,
        y: str = None,
        z: str = None,
        color_continuous_scale: List[str] = None,
        text_auto: bool = True,
        **kwargs
    ):
        """
        Initialize a heatmap.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            z: Column name for z-axis (values)
            color_continuous_scale: Color scale for continuous values
            text_auto: Whether to show text values automatically
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.z = z
        self.color_continuous_scale = color_continuous_scale or 'Viridis'
        self.text_auto = text_auto
        
    def create(self):
        """Create the heatmap."""
        if self.z is not None:
            # If z is provided, use it for values
            self.fig = px.density_heatmap(
                self.df,
                x=self.x,
                y=self.y,
                z=self.z,
                labels=self.labels,
                title=self.title,
                color_continuous_scale=self.color_continuous_scale,
                height=self.height,
                width=self.width,
                text_auto=self.text_auto
            )
        else:
            # If z is not provided, create a pivot table
            pivot_df = self.df.pivot_table(index=self.y, columns=self.x, aggfunc='size', fill_value=0)
            self.fig = px.imshow(
                pivot_df,
                labels=self.labels,
                title=self.title,
                color_continuous_scale=self.color_continuous_scale,
                height=self.height,
                width=self.width,
                text_auto=self.text_auto
            )
        
        # Update layout
        self.update_layout()
        return self


class AreaPlot(BaseChart):
    """Class for creating area plots."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str = None,
        line_group: str = None,
        groupnorm: str = None,
        **kwargs
    ):
        """
        Initialize an area plot.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color differentiation
            line_group: Column name for line grouping
            groupnorm: Group normalization ('fraction', 'percent')
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.line_group = line_group
        self.groupnorm = groupnorm
        
    def create(self):
        """Create the area plot."""
        self.fig = px.area(
            self.df,
            x=self.x,
            y=self.y,
            color=self.color,
            line_group=self.line_group,
            groupnorm=self.groupnorm,
            labels=self.labels,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width
        )
        
        # Update layout
        self.update_layout()
        return self


class BubblePlot(BaseChart):
    """Class for creating bubble plots."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        size: str,
        color: str = None,
        hover_name: str = None,
        log_x: bool = False,
        log_y: bool = False,
        size_max: int = 60,
        **kwargs
    ):
        """
        Initialize a bubble plot.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis
            y: Column name for y-axis
            size: Column name for bubble size
            color: Column name for color differentiation
            hover_name: Column name for hover labels
            log_x: Whether to use log scale for x-axis
            log_y: Whether to use log scale for y-axis
            size_max: Maximum size of bubbles
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.hover_name = hover_name
        self.log_x = log_x
        self.log_y = log_y
        self.size_max = size_max
        
    def create(self):
        """Create the bubble plot."""
        self.fig = px.scatter(
            self.df,
            x=self.x,
            y=self.y,
            size=self.size,
            color=self.color,
            hover_name=self.hover_name,
            log_x=self.log_x,
            log_y=self.log_y,
            size_max=self.size_max,
            labels=self.labels,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.color_sequence,
            height=self.height,
            width=self.width
        )
        
        # Update layout
        self.update_layout()
        return self


class RaincloudPlot(BaseChart):
    """Class for creating raincloud plots (combination of violin, box, and scatter)."""
    def __init__(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str = None,
        box_width: float = 0.1,
        violin_width: float = 0.6,
        point_size: int = 6,
        **kwargs
    ):
        """
        Initialize a raincloud plot.
        
        Args:
            df: DataFrame with the data
            x: Column name for x-axis (categorical)
            y: Column name for y-axis (numerical)
            color: Column name for color differentiation
            box_width: Width of box plots
            violin_width: Width of violin plots
            point_size: Size of scatter points
            **kwargs: Additional parameters for BaseChart
        """
        super().__init__(df, **kwargs)
        self.x = x
        self.y = y
        self.color = color
        self.box_width = box_width
        self.violin_width = violin_width
        self.point_size = point_size
        
    def create(self):
        """Create the raincloud plot (combination of violin, box, and scatter)."""
        # Create a figure with subplots
        self.fig = go.Figure()
        
        # Get unique categories
        categories = self.df[self.x].unique()
        
        # Create color mapping
        if self.color:
            color_values = self.df[self.color].unique()
            color_map = {val: self.color_sequence[i % len(self.color_sequence)] 
                         for i, val in enumerate(color_values)}
        
        # Add traces for each category
        for i, cat in enumerate(categories):
            cat_df = self.df[self.df[self.x] == cat]
            
            # Determine color
            if self.color:
                colors = [color_map[val] for val in cat_df[self.color]]
                color = self.color_sequence[i % len(self.color_sequence)]
            else:
                colors = [self.color_sequence[i % len(self.color_sequence)]] * len(cat_df)
                color = self.color_sequence[i % len(self.color_sequence)]
            
            # Add violin plot
            self.fig.add_trace(go.Violin(
                x=[cat] * len(cat_df),
                y=cat_df[self.y],
                name=cat,
                side='negative',
                width=self.violin_width,
                line_color=color,
                fillcolor=color,
                opacity=0.6,
                meanline_visible=True,
                showlegend=False
            ))
            
            # Add box plot
            self.fig.add_trace(go.Box(
                x=[cat] * len(cat_df),
                y=cat_df[self.y],
                name=cat,
                boxpoints=False,
                width=self.box_width,
                line_color=color,
                fillcolor='white',
                showlegend=False
            ))
            
            # Add scatter plot (jittered)
            jitter = np.random.normal(0, 0.05, size=len(cat_df))
            self.fig.add_trace(go.Scatter(
                x=[cat] * len(cat_df),
                y=cat_df[self.y],
                mode='markers',
                marker=dict(
                    color=colors,
                    size=self.point_size,
                    opacity=0.7
                ),
                name=cat,
                showlegend=(i == 0)  # Only show legend for first category
            ))
        
        # Update layout
        self.update_layout()
        return self


# Example usage
# def create_example_charts():
#     """Create example charts to demonstrate usage."""
#     # Sample data
#     # df = pd.DataFrame({
#     #     'Category': ['A', 'B', 'C', 'D', 'E'] * 3,
#     #     'Group': ['Group 1', 'Group 1', 'Group 1', 'Group 1', 'Group 1',
#     #              'Group 2', 'Group 2', 'Group 2', 'Group 2', 'Group 2',
#     #              'Group 3', 'Group 3', 'Group 3', 'Group 3', 'Group 3'],
#     #     'Value': [25, 38, 52, 45, 60, 40, 55, 70, 65, 80, 30, 45, 65, 70, 85],
#     #     'Error': [2, 3, 4, 3, 5, 3, 4, 5, 4, 6, 2, 3, 5, 4, 6],
#     #     'Size': [10, 20, 30, 25, 15, 25, 30, 35, 20, 25, 15, 25, 30, 35, 40],
#     #     'X': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
#     #     'Y': [10, 15, 13, 17, 20, 12, 18, 16, 22, 25, 15, 20, 18, 25, 30],
#     #     'Percentage': [10, 15, 25, 30, 20, 15, 20, 30, 25, 10, 20, 25, 15, 30, 10]
#     # })
#     # 
#     # # Example 1: Bar Chart
#     # bar = BarChart(
#     #     df=df,
#     #     x='Category',
#     #     y='Value',
#     #     color='Group',
#     #     text='Value',
#     #     title='Bar Chart Example',
#     #     x_title='Categories',
#     #     y_title='Values',
#     #     legend_title='Group'
#     # ).create()
#     # bar.display(use_streamlit=False, save_path='examples/bar_chart.png')
#     # 
#     # # Example 2: Pie Chart
#     # pie_df = df[df['Group'] == 'Group 1'].copy()
#     # pie = PieChart(
#     #     df=pie_df,
#     #     values='Value',
#     #     names='Category',
#     #     title='Pie Chart Example',
#     #     legend_title='Categories'
#     # ).create()
#     # pie.display(use_streamlit=False, save_path='examples/pie_chart.png')
#     # 
#     # # Example 3: Scatter Plot
#     # scatter = ScatterPlot(
#     pass