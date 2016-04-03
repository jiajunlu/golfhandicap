from fabric.api import local, prompt


def deploy():
    local('pip freeze > requirements.txt')
    local('git add .')
    comment = prompt("enter your git commit comment: ")
    local('git commit -m "%s"' % comment)
 #   local('git push -u origin master')
 #   local('heroku maintenance:on')
 #   local('git push heroku master')
 #   local('heroku maintenance:off')

