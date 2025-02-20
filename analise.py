import uuid
from helper import extract_data_analysis, get_pdf_paths, read_pdf
from database import AnalyseDatabase
from ai import GroqClient
from models.resum import Resum
from models.file import File
from models.analysis import Analysis
import download_cv
import authenticate


# Descarga de archivos ##
folder_id = '1PzWYRJmC4jaUIIFdCpKV0UGVMKBdu1fO'
download_cv.download_files_from_folder(folder_id)


database = AnalyseDatabase()
ai = GroqClient()
job = database.get_job_by_name('Vaga de Enfermeiro na Italia')

cv_paths = get_pdf_paths(directory="curriculos")
print(cv_paths)

for path in cv_paths:
    print(path)
    content = read_pdf(path)
    print(content)
    cv = content
    resum = ai.resume_cv(cv)
    opinion = ai.generate_opinion(content, job)
    print(opinion)
    score = ai.generate_score(resum, job)
    print(score)

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
    database.resums.insert(resum_schema.model_dump())
    database.files.insert(file_schema.model_dump())
    database.analysis.insert(analysis_schema.model_dump())


