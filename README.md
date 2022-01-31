TODO LIST:

- [ ] gestion d'erreur si l'access ipmi demandé n'est pas dispo coté ovh
- [ ] default value si ssh_key / ip pas set
- [ ] gestion d'erreur si OVH renvoie erreur
- [ ] parsing ip dans ipmi-config
- [ ] hint python
- [ ] better documentation
- [ ] support derniere version netbox


config:

```
PLUGINS_CONFIG = {
    'netbox_ipmi_ovh_plugin': {
        'ovh_server_name_field': 'existing field or custom field',
	'ovh_endpoint_field': 'existing or custom field',
        'endpoints': {
            'account1-ovh-eu': {
	        'endpoint': 'ovh-eu',
	        'application_key': 'xxxx',
		'application_secret': 'yyyy',
		'consumer_key': 'zzzz'
	    },
	    'account2-soyoustart-ca': {
	        'endpoint': 'soyoustart-ca',
	        'application_key': 'xxxx',
		'application_secret': 'yyyy',
		'consumer_key': 'zzzz'	    
	    }
        }
    }
}
```
