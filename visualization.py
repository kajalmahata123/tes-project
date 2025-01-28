# features/data_analysis/services/visualization.py
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

from smart_ql.features.data_analysis.models.models import VisualizationConfig


class AdvancedVisualizationService:
    def prepare_visualization(
            self,
            df: pd.DataFrame,
            chart_type: str,
            config: Dict
    ) -> VisualizationConfig:
        handlers = {
            'line': self._prepare_line_chart,
            'bar': self._prepare_bar_chart,
            'scatter': self._prepare_scatter_plot,
            'heatmap': self._prepare_heatmap,
            'box': self._prepare_box_plot,
            'bubble': self._prepare_bubble_chart,
            'area': self._prepare_area_chart,
            'radar': self._prepare_radar_chart,
            'funnel': self._prepare_funnel_chart,
            'treemap': self._prepare_treemap,
            'sankey': self._prepare_sankey_diagram,
            'candlestick': self._prepare_candlestick,
            'gauge': self._prepare_gauge_chart
        }

        handler = handlers.get(chart_type)
        if not handler:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        return handler(df, config)

    def _prepare_line_chart(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        x_axis = config['x_axis']
        y_axis = config['y_axis']

        data = df.groupby(x_axis)[y_axis].agg(['mean', 'min', 'max']).reset_index()
        return VisualizationConfig(
            type='line',
            data=data.to_dict('records'),
            title=f"{y_axis} over {x_axis}",
            x_axis=x_axis,
            y_axis=y_axis,
            options={
                'showArea': config.get('show_area', False),
                'showPoints': config.get('show_points', True),
                'showBounds': config.get('show_bounds', False)
            }
        )

    def _prepare_scatter_plot(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        x_axis = config['x_axis']
        y_axis = config['y_axis']

        correlation = df[x_axis].corr(df[y_axis])
        regression_line = None
        if config.get('show_regression', False):
            slope, intercept = np.polyfit(df[x_axis], df[y_axis], 1)
            regression_line = {'slope': slope, 'intercept': intercept}

        return VisualizationConfig(
            type='scatter',
            data=df[[x_axis, y_axis]].to_dict('records'),
            title=f"Correlation: {correlation:.2f}",
            x_axis=x_axis,
            y_axis=y_axis,
            options={
                'regression': regression_line,
                'showLabels': config.get('show_labels', False)
            }
        )

    def _prepare_heatmap(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        columns = config.get('columns', df.select_dtypes(include=[np.number]).columns)
        correlation_matrix = df[columns].corr()

        data = []
        for i, col1 in enumerate(columns):
            for j, col2 in enumerate(columns):
                data.append({
                    'x': col1,
                    'y': col2,
                    'value': correlation_matrix.iloc[i, j]
                })

        return VisualizationConfig(
            type='heatmap',
            data=data,
            title='Correlation Heatmap',
            x_axis='x',
            y_axis='y',
            options={
                'colorScale': config.get('color_scale', 'RdBu'),
                'showValues': config.get('show_values', True)
            }
        )

    def _prepare_box_plot(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        column = config['column']
        group_by = config.get('group_by')

        stats_data = []
        if group_by:
            for group in df[group_by].unique():
                group_data = df[df[group_by] == group][column]
                stats_data.append({
                    'group': group,
                    'min': group_data.min(),
                    'q1': group_data.quantile(0.25),
                    'median': group_data.median(),
                    'q3': group_data.quantile(0.75),
                    'max': group_data.max(),
                    'outliers': self._get_outliers(group_data)
                })
        else:
            data = df[column]
            stats_data.append({
                'group': column,
                'min': data.min(),
                'q1': data.quantile(0.25),
                'median': data.median(),
                'q3': data.quantile(0.75),
                'max': data.max(),
                'outliers': self._get_outliers(data)
            })

        return VisualizationConfig(
            type='box',
            data=stats_data,
            title=f'Distribution of {column}',
            x_axis='group',
            y_axis='value',
            options={
                'showOutliers': config.get('show_outliers', True),
                'showMean': config.get('show_mean', False)
            }
        )

    def _prepare_radar_chart(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        metrics = config['metrics']
        categories = config['categories']

        data = []
        for category in df[categories].unique():
            category_data = {'category': category}
            for metric in metrics:
                category_data[metric] = df[df[categories] == category][metric].mean()
            data.append(category_data)

        return VisualizationConfig(
            type='radar',
            data=data,
            title=config.get('title', 'Radar Chart'),
            x_axis='category',
            y_axis='metrics',
            options={
                'fillArea': config.get('fill_area', True),
                'showLabels': config.get('show_labels', True)
            }
        )

    def _prepare_sankey_diagram(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        source = config['source']
        target = config['target']
        weight = config.get('weight')

        flows = df.groupby([source, target]).size().reset_index(name='value') if not weight else \
            df.groupby([source, target])[weight].sum().reset_index()

        return VisualizationConfig(
            type='sankey',
            data=flows.to_dict('records'),
            title=config.get('title', 'Flow Diagram'),
            x_axis=source,
            y_axis=target,
            options={
                'nodeWidth': config.get('node_width', 20),
                'nodePadding': config.get('node_padding', 10)
            }
        )

    def _get_outliers(self, data: pd.Series) -> List[float]:
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        return list(data[(data < lower_bound) | (data > upper_bound)])

    def _prepare_bar_chart(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        x_axis = config['x_axis']
        y_axis = config['y_axis']
        group_by = config.get('group_by')

        if group_by:
            data = df.groupby([x_axis, group_by])[y_axis].agg('sum').reset_index()
        else:
            data = df.groupby(x_axis)[y_axis].agg(['sum', 'count']).reset_index()

        return VisualizationConfig(
            type='bar',
            data=data.to_dict('records'),
            title=f"{y_axis} by {x_axis}",
            x_axis=x_axis,
            y_axis=y_axis,
            options={
                'stacked': config.get('stacked', False),
                'horizontal': config.get('horizontal', False),
                'showValues': config.get('show_values', True),
                'groupBy': group_by
            }
        )

    def _prepare_bubble_chart(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        x_axis = config['x_axis']
        y_axis = config['y_axis']
        size = config['size']
        color = config.get('color')

        data = df[[x_axis, y_axis, size]].copy()
        if color:
            data['color'] = df[color]

        return VisualizationConfig(
            type='bubble',
            data=data.to_dict('records'),
            title=config.get('title', 'Bubble Chart'),
            x_axis=x_axis,
            y_axis=y_axis,
            options={
                'sizeField': size,
                'colorField': color,
                'showLabels': config.get('show_labels', False),
                'minSize': config.get('min_size', 5),
                'maxSize': config.get('max_size', 50)
            }
        )

    def _prepare_area_chart(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        x_axis = config['x_axis']
        y_axis = config['y_axis']
        stack_by = config.get('stack_by')

        if stack_by:
            data = df.pivot_table(
                values=y_axis,
                index=x_axis,
                columns=stack_by,
                aggfunc='sum'
            ).reset_index()
        else:
            data = df.groupby(x_axis)[y_axis].sum().reset_index()

        return VisualizationConfig(
            type='area',
            data=data.to_dict('records'),
            title=f"{y_axis} Area Chart",
            x_axis=x_axis,
            y_axis=y_axis,
            options={
                'stacked': config.get('stacked', True),
                'smooth': config.get('smooth', False),
                'fillOpacity': config.get('fill_opacity', 0.6),
                'stackBy': stack_by
            }
        )

    def _prepare_funnel_chart(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        stage = config['stage']
        value = config['value']

        data = df.groupby(stage)[value].sum().reset_index()
        data = data.sort_values(value, ascending=False)

        # Calculate conversion rates
        data['conversion_rate'] = data[value] / data[value].shift(-1) * 100

        return VisualizationConfig(
            type='funnel',
            data=data.to_dict('records'),
            title=config.get('title', 'Funnel Analysis'),
            x_axis=stage,
            y_axis=value,
            options={
                'showConversionRate': config.get('show_conversion_rate', True),
                'dynamicHeight': config.get('dynamic_height', True),
                'isTransposed': config.get('is_transposed', False)
            }
        )

    def _prepare_treemap(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        hierarchy = config['hierarchy']  # List of columns forming hierarchy
        size = config['size']
        color = config.get('color')

        def process_hierarchy(data, levels, current_level=0):
            if current_level >= len(levels):
                return []

            grouped = data.groupby(levels[current_level]).agg({
                size: 'sum',
                color: 'mean' if color else 'count'
            }).reset_index()

            result = []
            for _, row in grouped.iterrows():
                node = {
                    'name': row[levels[current_level]],
                    'value': row[size],
                    'color': row[color] if color else None
                }

                children = process_hierarchy(
                    data[data[levels[current_level]] == row[levels[current_level]]],
                    levels,
                    current_level + 1
                )

                if children:
                    node['children'] = children

                result.append(node)

            return result

        hierarchical_data = process_hierarchy(df, hierarchy)

        return VisualizationConfig(
            type='treemap',
            data=hierarchical_data,
            title=config.get('title', 'Treemap'),
            x_axis=hierarchy[0],
            y_axis=size,
            options={
                'colorField': color,
                'showLabels': config.get('show_labels', True),
                'hierarchyLevels': len(hierarchy)
            }
        )

    def _prepare_candlestick(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        date = config['date']
        open_price = config['open']
        high = config['high']
        low = config['low']
        close = config['close']
        volume = config.get('volume')

        data = df[[date, open_price, high, low, close]].copy()
        if volume:
            data['volume'] = df[volume]

        # Add technical indicators if requested
        if config.get('show_ma'):
            data['MA20'] = df[close].rolling(window=20).mean()
            data['MA50'] = df[close].rolling(window=50).mean()

        return VisualizationConfig(
            type='candlestick',
            data=data.to_dict('records'),
            title=config.get('title', 'Price Chart'),
            x_axis=date,
            y_axis='price',
            options={
                'showVolume': volume is not None,
                'showMA': config.get('show_ma', False),
                'upColor': config.get('up_color', '#26A69A'),
                'downColor': config.get('down_color', '#EF5350')
            }
        )

    def _prepare_gauge_chart(self, df: pd.DataFrame, config: Dict) -> VisualizationConfig:
        value = config['value']
        min_value = config.get('min', df[value].min())
        max_value = config.get('max', df[value].max())

        current_value = df[value].iloc[-1] if len(df) > 0 else 0

        # Calculate ranges for color zones
        range_size = (max_value - min_value) / 3
        ranges = [
            {'from': min_value, 'to': min_value + range_size, 'color': '#FF4D4F'},
            {'from': min_value + range_size, 'to': max_value - range_size, 'color': '#FAAD14'},
            {'from': max_value - range_size, 'to': max_value, 'color': '#52C41A'}
        ]

        return VisualizationConfig(
            type='gauge',
            data=[{
                'value': current_value,
                'min': min_value,
                'max': max_value
            }],
            title=config.get('title', 'Gauge Chart'),
            x_axis='value',
            y_axis='value',
            options={
                'ranges': ranges,
                'showPercentage': config.get('show_percentage', True),
                'startAngle': config.get('start_angle', 180),
                'endAngle': config.get('end_angle', 0)
            }
        )