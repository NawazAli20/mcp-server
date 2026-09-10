## Create a simple MCP server 

from pathlib import Path
import json
from typing import Any

from mcp.server.fastmcp import FastMCP

##get the data file 
DATA_FILE = Path(__file__).resolve().parent/"data"/"courses.json"


#read the file 
def _load_courses()->list[dict[str,Any]]:
    """Load courses from file and return as a list"""
    try:
        with DATA_FILE.open(encoding="utf-8") as file: 
            courses = json.load(file)
            return courses
    except Exception as e: 
        return f"data file reading error"

def _normalize_course_id(course_id:str)->str:
    """convert a course id in the form of CS111"""
    formated_course_id = "".join(course_id.upper().split())
    return formated_course_id

##instantiate mcp 
mcp = FastMCP(
    name="Course Assistant",
    instructions="""Use these tools to retrieve list of courses and course details 
    of a given course"""
)

@mcp.tool()
def get_course_list()->list[dict[str,Any]]:
    """Return the list of available courses"""
    return [
        {
            "Course_id":course["course_id"],
            "Title":course["title"]
        }
        for course in _load_courses()
    ]

@mcp.tool()
def get_course_details(course_id:str)->dict[str,Any]:
    """Return the details of a given course if found"""
    normalize_course_id = _normalize_course_id(course_id)
    for course in _load_courses():
        if (_normalize_course_id(course["course_id"]) == normalize_course_id):
            return course

    # if the given course is not found return the list of available course id
    available_course_id = [course["course_id"] for course in _load_courses()]
    return {
        "Error":f"{course_id} is not available",
        "Avilable_courses":available_course_id
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")

    #print(_load_courses())
    #print(_normalize_course_id(" cs 111"))
    #print(get_course_list())
    #print(get_course_details("cs 112"))