# import relevant dependencies for backend server
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
import os, shutil, uuid
from fastapi.middleware.cors import CORSMiddleware


# import pdf editor library
import pymupdf

# Setup backend server
app = FastAPI()

# Middleware to allow backend to receive requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
def root():
    return {"status": "Backend is live"}



def highlight_words_in_pdf(input_pdf, output_pdf, word_color_map):
    doc = pymupdf.open(input_pdf)
    for page in doc:
        for entry in word_color_map:
            color = entry["color"]
            for word in entry["terms"]:
                text_instances = page.search_for(word)
                for inst in text_instances:
                    # Highlighter of words
                    annot = page.add_rect_annot(inst)
                    annot.set_colors(stroke=pymupdf.pdfcolor[color], fill=pymupdf.pdfcolor[color])
                    annot.update(opacity=0.5)
                    
                    # Adds text annotation pop-ups
                    annot = page.add_text_annot(
                                    inst.tl,  # top-left corner of the found text rectangle
                                    entry["var"]
                                )
                    # Gets rid of icon
                    annot.update(opacity=0)

                    annot.update()  # Final Save/Update
    doc.save(output_pdf)

# Usage example
word_color_map = [
    {
    #  Cargiver Relationship
        "var": "Variable 1: Caregiver Relationship Status",
        "terms": ["the", "reciprocity", "primary caregiver", "emotional support", "role strain", "role conflict", "structural ambivalence", "psychological ambivalence"],
        "color": "pink"
    },
    {
        # Gender
        "var": "Variable 2: Gender",
        "terms": ["sex", "gender roles", "gender identity", "social context", "cultural context", "expectations", "role strain", "gender disparities", "social norms"],
        "color": "green"
    } # ,
    #  {
    #     # Marriage
    #     "terms": ["Married", "single", "divorced", "widowed", "separated", "never married", "in a relationship", "engaged", "cohabitation", "cohabitating", "remarried", "relationship status", "marital status", "long-term partner", 
    #               "married with children", "married without children", "legally married", "divorced", "relationship history", "spouse", "partner"],
    #     "color": "blue"
    # },
    #  {
    #     # Income
    #     "terms": ["income", "Annual income", "household income", "income level", "personal income", "income range", "tax-bracket", "income bracket", "yearly earnings", "low-income", "middle-income", "high-income", "poverty line", "financial status", "wage", "salary", "earnings", "socio-economic status", "economic background", "financial bracket", "disposable income"],
    #     "color": "red"
    # },
    #  {
    #     # Close relationship Quality
    #     "terms": ["Trust", "Emotional Support", "Intimacy", "Companionship", "Support", "Loneliness", "Conflict", "Dependability", "Attachment", "Empathy"],
    #     "color": "gray"
    # },
    #  {
    #     # Comorbid Conditions
    #     "terms": ["Illness", "Chronic Illness", "Condition", "Diagnosis", "Disease", "Impairment", "Multimorbidity", "Disability", "Health", "Acute Illness", "Comorbidity", "Psychiatric Disorder", "Health Status"],
    #     "color": "yellow"
    # },
    # {
    #     # Race
    #     "terms": ["Race", "Ethnicity", "Heritage", "Ancestry", "Lineage Background", "Cultural identity", "Demographic group", "Origins", "Descent", "People group"],
    #     "color": "purple"
    # },
    # {
    #     # Age
    #     "terms": ["Age", "Lifespan", "years", "maturity", "era", "stage of life", "generation", "time of life", "chronological age", "seniority", "life cycle"],
    #     "color": "orange"
    # }
    ]


# Define route for backend requests
@app.post("/annotate/")


async def annotate(file: UploadFile = File(...)):
    # store input and output files in temp folder
    os.makedirs("temp", exist_ok=True)
    temp_id = str(uuid.uuid4())
    input_path = f"temp/{temp_id}.pdf"
    output_path = f"temp/{temp_id}_annotated.pdf"

    # Save uploaded file to disk
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Annotate the PDF
    highlight_words_in_pdf(input_path, output_path, word_color_map)

    # Prepare file to return to client
    def file_iterator(file_path):
        with open(file_path, mode="rb") as f:
            yield from f

        # Clean up both input and output after sending
        os.remove(input_path)
        os.remove(output_path)

    return StreamingResponse(
        file_iterator(output_path),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=annotated.pdf"}
    )
