import web
import json
import traceback
import sqlite3

from api_utils import simple_response_validation, \
    ForcePushInfoDTO, validate_signature
from utils import find_force_push_events_for_ref, get_db_path


class force_pushes_for_ref:
    """
    This endpoint takes a ref such as a branch name (branch test would be
    'refs/heads/deleteme-test') and returns list of dicts with data on
    all force push events received for this ref
    """
    def POST(self):
        data = web.data()
        if len(data) > 255:
            raise web.webapi.BadRequest()
        rows = find_force_push_events_for_ref(data)
        results = [ForcePushInfoDTO.from_db_row(row).to_dict for row in rows]
        web.header('Content-type', 'application/json')
        return json.dumps(results)


class force_pushes_for_branch:
    """
    This endpoint takes a branch name and returns list of dicts with data on
    all force push events received for this branch
    """
    def POST(self):
        data = web.data()
        if len(data) > 255:
            raise web.webapi.BadRequest()
        rows = find_force_push_events_for_ref('refs/heads/'+data)
        results = [ForcePushInfoDTO.from_db_row(row).to_dict for row in rows]
        web.header('Content-type', 'application/json')
        return json.dumps(results)


class hook:
    """
    Github push event hook endpoint.

    Save any force push events received to db, keyed on the ref string so that
    you can look up force pushes by ref string later.
    """
    @validate_signature
    def POST(self):
        # todo add ping event response

        data = web.data()
        try:
            data_dict = json.loads(data)
        except:
            print 'Invalid json received'
            traceback.print_exc()
            raise web.webapi.BadRequest()

        if data_dict.get('forced') is not True:
            # only save force pushes, so ignore other push events
            raise web.webapi.ok()

        simple_response_validation(data_dict)

        conn = sqlite3.connect(get_db_path())
        ref = str(data_dict.get('ref'))
        repo_name = str(data_dict.get(
            'repository', {}).get('full_name'), '<name_missing>')
        conn.execute('INSERT INTO data(repo_name,ref,event) VALUES (?,?,?)', (repo_name, ref, data))
        conn.commit()
        conn.close()
        return web.webapi.Accepted()
