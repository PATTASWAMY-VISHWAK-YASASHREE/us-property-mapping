from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.report import Report
from app.schemas.report import (
    Report as ReportSchema,
    ReportCreate,
    ReportUpdate,
    ReportTemplate
)

router = APIRouter()

@router.get("/", response_model=List[ReportSchema])
def list_reports(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve reports.
    """
    reports = db.query(Report).filter(
        Report.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return reports

@router.post("/", response_model=ReportSchema)
def create_report(
    *,
    db: Session = Depends(get_db),
    report_in: ReportCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new report.
    """
    report = Report(
        user_id=current_user.id,
        name=report_in.name,
        report_type=report_in.report_type,
        parameters=report_in.parameters,
        scheduled=report_in.scheduled,
        schedule_frequency=report_in.schedule_frequency,
        status="pending"  # Initial status
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    
    # In a real implementation, we would trigger a background task to generate the report
    # but for simplicity we'll just return the created report
    
    return report

@router.get("/{report_id}", response_model=ReportSchema)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific report by id.
    """
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    *,
    db: Session = Depends(get_db),
    report_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a report.
    """
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    db.delete(report)
    db.commit()
    
    return None

@router.post("/schedule", response_model=ReportSchema)
def schedule_report(
    *,
    db: Session = Depends(get_db),
    report_id: int = Body(...),
    schedule_frequency: str = Body(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Schedule a report to run periodically.
    """
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Update report schedule
    report.scheduled = True
    report.schedule_frequency = schedule_frequency
    db.commit()
    db.refresh(report)
    
    return report

@router.get("/templates", response_model=List[ReportTemplate])
def get_report_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get available report templates.
    """
    # In a real implementation, we would fetch templates from the database
    # but for simplicity we'll just return dummy data
    
    templates = [
        ReportTemplate(
            id="property-valuation",
            name="Property Valuation Report",
            description="Analyze property values in a specific area",
            report_type="property",
            parameters_schema={
                "location": {"type": "string", "required": True},
                "radius": {"type": "number", "required": True},
                "property_types": {"type": "array", "items": {"type": "string"}}
            }
        ),
        ReportTemplate(
            id="wealth-analysis",
            name="Wealth Analysis Report",
            description="Analyze wealth distribution of property owners",
            report_type="wealth",
            parameters_schema={
                "min_property_value": {"type": "number"},
                "location": {"type": "string"},
                "owner_types": {"type": "array", "items": {"type": "string"}}
            }
        ),
        ReportTemplate(
            id="market-trends",
            name="Market Trends Report",
            description="Analyze property market trends over time",
            report_type="market",
            parameters_schema={
                "location": {"type": "string", "required": True},
                "time_period": {"type": "string", "enum": ["1y", "3y", "5y", "10y"]},
                "property_types": {"type": "array", "items": {"type": "string"}}
            }
        )
    ]
    
    return templates