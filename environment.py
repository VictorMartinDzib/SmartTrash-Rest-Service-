'''
    Variables de entorno para la configuracion del servicio.
    Environment variables to config the service.
'''

setup = {
    'host':'localhost',
    'port': 9986,
    'debug': True
}

database = {
    'host':setup['host'],
    'port':5517,
    'dbname':'smartTrash',
    'gestor':'mongodb'
}