packages:
  pkg.installed:
    - names:
      - git
      - tmux
      - salt-master
      - python-dev
      - python-pip
      - python-virtualenv

print_user:
  cmd.run:
    - name: "echo 'Using user: {{ pillar['user'] }}'"

# Clone git repo
https://github.com/danielfrg/semafor-parsing:
  git.latest:
    - user: {{ pillar['user'] }}
    - target: /home/{{ pillar['user'] }}/semafor/app

# --------------------------------------------------------------------
#                             RabbitMQ

rabbitmq-server:
  pkgrepo.managed:
    - humanname: Rabbitmq PPA
    - name: deb http://www.rabbitmq.com/debian/ precise main
  pkg:
    - installed
  service:
    - running

# --------------------------------------------------------------------
#                              Python

/home/{{ pillar['user'] }}/venv:
  virtualenv.managed:
    - user: {{ pillar['user'] }}
    - system_site_packages: True
    - pip: True

celery:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

boto:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

luigi:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

tornado:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

daemon:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv






