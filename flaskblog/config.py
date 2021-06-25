import os

class Config:
	SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
	SQLALCHEMY_DATABASE_URI = 'mysql://root:Administrator@13aug@localhost/blog'
	LDAP_PROVIDER_URL = 'LDAP://ericsson.se'
	LDAP_PROTOCOL_VERSION = 3