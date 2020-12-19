from fabric.api import local


PROJECT_NAME = 'flaskr'


def runserver():
    try:
        local(f'docker rm -f {PROJECT_NAME}_server')
    except:
        pass
    finally:
        local(f'docker-compose run --name {PROJECT_NAME}_server --service-ports --use-aliases server poetry run flask run --host=0.0.0.0 --port=8000')


def test(path='.'):
    try:
        local(f'docker rm -f {PROJECT_NAME}_server')
    except:
        pass
    finally:
        local(f'docker-compose run --name {PROJECT_NAME}_server --use-aliases server poetry run pytest -s {path}')


def bash(service_name):
    local(f'docker exec -it {PROJECT_NAME}_{service_name} bash')

def initdb():
    local(f'docker exec -it {PROJECT_NAME}_server poetry run flask init-db')
