# Copyright (c) 2012-2016 Seafile Ltd.
# encoding: utf-8

import logging

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django.db import connection

from seaserv import seafile_api, ccnet_api

from seahub.utils import is_pro_version
from seahub.utils.file_size import get_file_size_unit
from seahub.utils.ms_excel import write_xls
from seahub.constants import GUEST_USER, DEFAULT_USER
from seahub.base.models import UserLastLogin
from seahub.base.templatetags.seahub_tags import tsstr_sec
from seahub.profile.models import Profile

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Shen Hang DEPT Sync"

    def add_arguments(self, parser):
        parser.add_argument('db_name', type=str)

    def handle(self, *args, **options):
        self.db_name = options.get('db_name')
        if not self.db_name:
            logger.error('db_name invalid')
            return
        try:
            self.sync_dept(self.db_name)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('E = {}'.format(e))


    def get_children_by_parent_id(self, parent_id):
        sql = 'SELECT DWH, DWMC FROM {}.YXSDWJBSJXX WHERE LSDWH="{}" AND DWH!="{}"'.format(self.db_name, parent_id, parent_id)
        print('sql = ' + sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        print('res = {}'.format(res))
        return res



    def get_sub_depts(self, parent_dept_id):
        current_tree_node = {}

        current_node_id_list = self.get_children_by_parent_id(parent_dept_id)
        print('current_node_id_list = {}'.format(current_node_id_list))
        # for id in current_node_id_list:
        #     current_tree_node[id] = self.get_sub_depts(id)
        #
        # return current_tree_node
        for id, name in current_node_id_list:
            current_tree_node[name] = self.get_sub_depts(id)
        return current_tree_node


    def sync_dept(self, db_name):
        print('in sycn org db_name = ' + db_name)
        sql = 'SELECT DWH, DWMC, LSDWH FROM {}.YXSDWJBSJXX'.format(db_name)
        print('sql = ' + sql)
        self.dept_tree = {}
        # with connection.cursor() as cursor:
        # # cursor.execute(sql)
        # # res = cursor.fetchall()

        top_dep_id = 'A'
        top_dep_name = '沈阳航空航天大学'
        self.dept_tree[top_dep_name] = self.get_sub_depts(top_dep_id)
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        self.dfs_dept_tree(self.dept_tree, parent_group_id=-1)

    def dfs_dept_tree(self, current_node, parent_group_id):
        for k, v in current_node.items():
            print('k = ' + k)
            group_id = ccnet_api.create_group(group_name=k, user_name='admin', parent_group_id=parent_group_id)
            self.dfs_dept_tree(v, group_id)








