{% if not salt['cmd.run']('id -u "vagrant"').endswith('No such user') %}
user: vagrant
{% else %}
user: ubuntu
{% endif %}