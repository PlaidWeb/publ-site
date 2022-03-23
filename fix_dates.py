""" Fix filename dates """

import time
import os
import os.path
from app import app
from publ import model, index
from publ.config import config
import re
import arrow
from pony import orm

def reindex():
    with app.app_context():
        print('Indexing', end='', flush=True)
        index.scan_index(config.content_folder, False)
        n = 0
        while index.in_progress():
            n += 1
            if n % 5 == 0:
                print('.', end='', flush=True)
            time.sleep(0.1)
        print('Done')


reindex()

fix_count = 0

with orm.db_session:
    for entry in model.Entry.select(category='blog'):
        dirname = os.path.dirname(entry.file_path)
        basename, ext = os.path.splitext(os.path.basename(entry.file_path))

        match = re.match(r'([0-9\-.A-Z]+[0-9A-Z])(.*)', basename)
        if match:
            status = model.PublishStatus(entry.status)
            if status not in (model.PublishStatus.PUBLISHED, model.PublishStatus.SCHEDULED):
                eid = status.name
            else:
                eid = entry.id

            date = arrow.get(entry.local_date).format('YYYYMMDD')

            if status == model.PublishStatus.HIDDEN:
                prefix = f'HIDDEN-{entry.id}'
            elif status == model.PublishStatus.DRAFT:
                prefix = 'DRAFT'
            else:
                prefix = f'{date}-{eid}'

            if prefix != match.group(1):
                dest_name = f'{prefix}{match.group(2)}'
                print(f'{entry.category} {basename} -> {dest_name}')
                dest_path = os.path.join(dirname, dest_name + ext)
                os.rename(entry.file_path, dest_path)
                fix_count += 1

if fix_count > 0:
    print(f'{fix_count} files renamed')
    reindex()
