# Data explorer

In order to complement the results of our paper _Evolutionary cues from physicochemical features of proteomes alone_, this website was built as a tool for any reader to directly explore the data much in the same way as I did during the study.

## Scope

## Usage

## Technical notes
Backend was developed in Django3.7.

Frontend relies on a single `main.js` and Bootstrap4.0 utilities.

Deployed to Heroku on September 2021.

### Heroku
Heroku's repo for this project can be cloned using: `heroku git:clone -a proteome-explorer` or **preferably** from https://github.com/eloyvallinaes/proteome-data-explorer.git.

### Database
While an sqlite3 database was used during development, Heroku doesn't admit static
databases, so all of the data needed to be migrated to a remote postgresql database.
This process involved:
1. Loading data to sqlite3 database; see [`pandas.DataFrame.to_sql`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html).
2. Letting Django infer the appropriate models for the data; see [`python3 manage.py inspectdb`](https://docs.djangoproject.com/en/3.2/howto/legacy-databases/).
3. Dumping the data to a properly formatted fixture with [`django-admin dumpdata`](https://docs.djangoproject.com/en/3.2/ref/django-admin/), preferably excluding additional tables like `contenttypes` or `sessions` if present. For instance:
```
python3 manage.py dumpdata --database default --indent 4 -e contenttypes -e auth -e sessions > dataDump.json
```
4. Creating a postgresql service at Heroku and connecting app to that database:
```
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'denf2r0kqefnt6',
        'USER': 'fyzcwycdylfviv',
        'PASSWORD': '5a7786cfa3117aff2feb86e93459170c865c2694e03782fcfa248461a1a1d966',
        'HOST': 'ec2-54-155-254-112.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}
```
5. Loading fixture to remote database with `django-admin loaddata`. For a fixture containing 18000+ rows, this takes several minutes; be patient.
6. Upgrade Heroku postgresql database from hobby-dev to **hobby-basic**, since it contains too many rows for the free plan (limited to 1000). See [updating database](https://devcenter.heroku.com/articles/upgrading-heroku-postgres-databases#upgrading-with-pg-copy).

#### Changing data
Updates can be issued to database ```Props``` table with ```scripts/load_data.py```. After that, steps 3 and 5 from the above list need to be repeated.
