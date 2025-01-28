# features/data_analysis/models.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class VisualizationConfig(BaseModel):
    type: str
    data: List[Dict]
    title: str
    x_axis: str
    y_axis: str
    options: Optional[Dict] = None

class AnalysisRequest(BaseModel):
    query_results: List[Dict]
    analysis_type: str = 'comprehensive'
    include_visualizations: bool = True

class AnalysisResponse(BaseModel):
    eda_results: Dict
    visualizations: List[VisualizationConfig]
    deep_insights: Dict
