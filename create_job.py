import uuid
from models.job import Job
from database import AnalyseDatabase

database = AnalyseDatabase()
name = "Vaga de Enfermeiro em Italia"

activities = '''
Cuidados e assistência a idosos em ambiente residencial.
Administração de medicamentos e monitoramento das condições de saúde.
Colaboração com médicos e outros profissionais de saúde.
Planejamento e execução de atividades recreativas e terapêuticas.
Manutenção de registros médicos e relatórios de progresso.
'''

prerequisites = '''
Licença de enfermeiro no Brasil.
Experiência prévia no cuidado de idosos.
Conhecimentos em administração de medicamentos.
Habilidades de comunicação efetiva.
Capacidade de trabalhar em equipe e lidar com situações de emergência.
'''

differentials = '''
Formação contínua em cuidados com idosos.
Idiomas adicionais (espanhol, inglês).
Experiência em técnicas de reabilitação.
Conhecimentos em tecnologia médica avançada.
Certificações adicionais em cuidados gerontológicos.
'''

job = Job(
    id = str(uuid.uuid4()),
    name = name,
    main_activities=activities,
    prerequisites=prerequisites,
    differentials=differentials
)

database.jobs.insert(job.model_dump())