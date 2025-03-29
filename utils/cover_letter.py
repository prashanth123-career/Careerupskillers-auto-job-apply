from transformers import pipeline

# Try to load a lightweight model for cover letter generation
try:
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
except Exception as e:
    print("⚠️ Model load failed:", e)
    generator = None

# Function to generate a cover letter using the resume and job title
def generate_cover_letter(resume_text, job_title):
    if generator is None:
        return "⚠️ Could not load the AI model. Please try again later."

    prompt = f"Write a professional cover letter for the position of '{job_title}' based on the following resume:\n\n{resume_text}"
    result = generator(prompt, max_length=300, do_sample=True, temperature=0.7)
    return result[0]['generated_text']
