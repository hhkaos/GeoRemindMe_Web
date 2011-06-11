Last update: 11st June 2011

The GeoRemindMe translation project is hosted at:
https://www.transifex.net/projects/p/georemindme/

Go there to get any file with .po translations

====================================================================

How to update languages:

There is 2 scripts at /trunk/src/webapp directory:

1) update_strings.py 
2) compile_strings.py

** How to run **:
chmod +x update_strings.py compile_strings.py
./update_strings.py
./compile_strings.py

OR:
python update_strings.py
python compile_strings.py

IMPORTANT:
You must run script (1) in case you change any public string that must be translated again before any push.

And you must run script (2) after changing any .po file.


====================================================================
Information about how to create .po and .mo files:
http://docs.djangoproject.com/en/dev/topics/i18n/localization/

You need to have installed this:
sudo apt-get install gettext

django-admin.py makemessages -l de #creates german (de) .po
django-admin.py compilemessages # compiles and create .mo

or
django-admin makemessages -l es #creates spanish (es) .po
django-admin compilemessages # compiles and create .mo

how to create translation strings:
http://docs.djangoproject.com/en/dev/topics/i18n/internationalization/#

http://docs.djangoproject.com/en/dev/howto/i18n/#using-translations-in-your-own-projects
