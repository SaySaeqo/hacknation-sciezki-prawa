from fastapi import FastAPI
from scraper import get_projects_list, get_project_details, get_stage_details

app = FastAPI(title="Legislative API", description="API for scraping legislative data from rcl.gov.pl")

@app.get("/projects")
def get_projects():
    return get_projects_list()

@app.get("/project/{project_id}")
def get_project(project_id: int):
    return get_project_details(project_id)

@app.get("/project/{project_id}/stage/{katalog_id}")
def get_stage(project_id: int, katalog_id: int):
    return get_stage_details(project_id, katalog_id)