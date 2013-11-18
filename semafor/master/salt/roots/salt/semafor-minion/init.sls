packages:
  pkg.installed:
    - names:
      - git
      - maven
      - python-dev
      - python-pip
      - python-virtualenv
      - openjdk-6-jdk

print_user:
  cmd.run:
    - name: "echo 'Using user: {{ pillar['user'] }}'"

# Clone git repo
https://github.com/danielfrg/semafor-parsing:
  git.latest:
    - user: {{ pillar['user'] }}
    - target: /home/{{ pillar['user'] }}/semafor/app

# --------------------------------------------------------------------
#                              Python

/home/{{ pillar['user'] }}/venv:
  virtualenv.managed:
    - user: {{ pillar['user'] }}
    - system_site_packages: false
    - pip: True

celery:
  pip.installed:
    - bin_env: /home/{{ pillar['user'] }}/venv

luigi:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

requests:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

nltk:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

beautifulsoup4:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

boto:
  pip.installed:
    - user: {{ pillar['user'] }}
    - bin_env: /home/{{ pillar['user'] }}/venv

# --------------------------------------------------------------------
#                             Semafor

# Clone git repo
https://github.com/sammthomson/semafor:
  git.latest:
    - user: {{ pillar['user'] }}
    - rev: 266453f0428b31811fdde1123b5be893b62928e6
    - target: /home/{{ pillar['user'] }}/semafor/semafor

# Check if need .jar exists
semafor_check:
  cmd.run:
    - name: "[ -e /home/{{ pillar['user'] }}/semafor/semafor/target/Semafor-3.0-alpha-04.jar ] && echo 'changed=no' || echo 'changed=yes'"
    - stateful: True

# If jar does not exists, run `mvn package`
semafor_compile:
  cmd.wait:
    - name: "mvn package"
    - user: {{ pillar['user'] }}
    - cwd: /home/{{ pillar['user'] }}/semafor/semafor
    - watch:
        - cmd: semafor_check

# Download malt model
semafor_malt_model_file:
  file.managed:
    - user: {{ pillar['user'] }}
    - name: /home/{{ pillar['user'] }}/semafor/models/malt.tar.gz
    - source: http://www.ark.cs.cmu.edu/SEMAFOR/semafor_malt_model_20121129.tar.gz
    - source_hash: md5=1632e586685494013a092cd4cff679f5

# Check if need malt_model_dir exists
semafor_malt_check:
  cmd.run:
    - name: "[ -d /home/{{ pillar['user'] }}/semafor/models/semafor_malt_model_20121129 ] && echo 'changed=no' || echo 'changed=yes'"
    - stateful: True

# Untar malt model
semafor_malt_model_untar:
  cmd.wait:
    - user: {{ pillar['user'] }}
    - name: "tar -zxvf /home/{{ pillar['user'] }}/semafor/models/malt.tar.gz"
    - cwd: /home/{{ pillar['user'] }}/semafor/models
    - watch:
      - cmd: semafor_malt_check








