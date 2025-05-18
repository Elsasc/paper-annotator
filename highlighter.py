import pymupdf  

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

highlight_words_in_pdf("inp2.pdf", "out2.pdf", word_color_map)
print("Success")
