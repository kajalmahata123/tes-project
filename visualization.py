from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, List, Optional
from pydantic import BaseModel
import pandas as pd

from smart_ql.features.data_analysis.services.analyzer import AdvancedDataAnalyzer
from smart_ql.features.data_analysis.services.visualization import AdvancedVisualizationService

data_analysis_router = APIRouter()


class AnalysisRequest(BaseModel):
    data: List[Dict]
    analysis_type: str = 'comprehensive'
    visualization_types: Optional[List[str]] = None


class DataResponse(BaseModel):
    analysis_results: Dict
    visualizations: List[Dict]


@data_analysis_router.post("/analyze", response_model=DataResponse)
async def analyze_data(
        request: AnalysisRequest,
        analyzer: AdvancedDataAnalyzer = Depends(),
        viz_service: AdvancedVisualizationService = Depends()
) -> Dict:
    try:
        df = pd.DataFrame(request.data)

        analysis_results = await analyzer.analyze_data(
            df=df,
            analysis_type=request.analysis_type
        )

        visualizations = []
        if request.visualization_types:
            for viz_type in request.visualization_types:
                viz_config = viz_service.prepare_visualization(
                    df=df,
                    chart_type=viz_type,
                    config=analysis_results.get('visualization_config', {})
                )
                visualizations.append(viz_config)

        return {
            "analysis_results": analysis_results,
            "visualizations": visualizations
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@data_analysis_router.post("/visualize")
async def get_visualizations(
        request: AnalysisRequest,
        viz_service: AdvancedVisualizationService = Depends()
) -> Dict:
    try:
        df = pd.DataFrame(request.data)
        visualizations = []

        for viz_type in request.visualization_types or ['bar', 'line']:
            viz_config = viz_service.prepare_visualization(
                df=df,
                chart_type=viz_type,
                config={}
            )
            visualizations.append(viz_config)

        return {"visualizations": visualizations}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
