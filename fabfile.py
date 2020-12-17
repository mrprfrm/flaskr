from fabric.api import local


PROJECT_NAME = 'flaskr'


def bash(service_name):
    local(f'docker exec -it {PROJECT_NAME}_{service_name} bash')

def initdb():
    local(f'docker exec -it {PROJECT_NAME}_server poetry run flask init-db')
