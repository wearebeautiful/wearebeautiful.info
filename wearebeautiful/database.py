import os
import json

from peewee import SqliteDatabase
from wearebeautiful.db_model import DBModel, db, create_from_manifest
from wearebeautiful.manifest import validate_manifest

def add_models(dir):
    for item in os.listdir(dir):
        print(item)
        if item.endswith(".json"): 
            with(open(os.path.join(dir, item), "rb")) as m:
                try:
                    manifest = json.loads(str(m.read().decode('utf-8')))
                except json.decoder.JSONDecodeError as err:
                    print("  skipping. %s" % (item, str(err)))
                    continue
                except IOError as err:
                    print("  skipping. %s" % (item, str(err)))
                    continue

            err = validate_manifest(manifest)
            if err:
                print("  manifest not valid, skipping: %s" % err)
                continue

            print("add file to db")
            model = create_from_manifest(manifest)
            model.save()


def add_human_model(dir):
    for item in os.listdir(dir):
        dir_name = os.path.join(dir, item)
        print(dir_name)
        if len(item) == 11 and item[0:6].isdigit() and \
            item[6] == '-' and os.path.isdir(dir_name):
            add_models(dir_name)


def create_database(db_file, model_archive):
    db.init(db_file)
    db.create_tables([DBModel])
    for item in os.listdir(model_archive):
        dir_name = os.path.join(model_archive, item)
        if len(item) == 6 and item.isdigit() and os.path.isdir(dir_name):
            add_human_model(dir_name)
