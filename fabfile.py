from fabric.api import local
        def save():
        local('git add .')
        local('git commit -a')
        def updatedb(app):
        local('./manage.py schemamigration '+app+' --auto')
        local('./manage.py migrate '+app)
