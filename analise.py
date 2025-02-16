import uuid
from helper import extract_data_analysis, get_pdf_paths, read_pdf
from database import AnalyseDatabase
from ai import GroqClient
from models.resum import Resum

database = AnalyseDatabase()
ai = GroqClient
job = database.get_job_by_name('Vaga de Enfermeiro na Italia')

cv_paths = get_pdf_paths(directory="curriculos")

for path in cv_paths:
    content = read_pdf(path)
    resum = ai.resume_cv(content)
    opinion = ai.generate_opinion(content)
    score = ai.generate_score(content, job)

    resum_schema = Resum(
        id = str(uuid.uuid4()),
        job_id=job.get('id'),
        content=resum,
        file=str(path),
        opinion=opinion
    )

    file_schema = File(
        file_id=str(uuid.uuid4()),
        job_id=job.get('id')
    )

    analysis_schema = extract_data_analysis(resum, job.get('id'), resum_schema.id, score)
    database.resums.insert(resum_schema.model_dump)
    database.files.insert(file_schema.model_dump)


