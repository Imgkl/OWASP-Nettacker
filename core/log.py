#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
import sys
from core.alert import messages
from core.alert import info
from core.alert import error
from core import compatible

try:
    import texttable
except:
    from core.color import finish

    error('pip install -r requirements.txt')
    finish()
    sys.exit(1)


def build_graph(graph_flag, language, data, _HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION):
    info(messages(language, 88))
    try:
        start = getattr(
            __import__('lib.graph.%s.engine' % (graph_flag.rsplit('_graph')[0]),
                       fromlist=['start']),
            'start')
    except:
        error(messages(language, 98).format(graph_flag))
        from core.color import finish
        finish()
        sys.exit(1)

    info(messages(language, 89))
    return start(graph_flag, language, data, _HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION)


def _get_log_values(log_in_file):
    o = open(log_in_file)
    data = ''
    for value in o:
        if value[0] == '{':
            data += value + ','
    return data[:-1]


def sort_logs(log_in_file, language, graph_flag):
    _HOST = messages(language, 53)
    _USERNAME = messages(language, 54)
    _PASSWORD = messages(language, 55)
    _PORT = messages(language, 56)
    _TYPE = messages(language, 57)
    _DESCRIPTION = messages(language, 58)
    if compatible.version() is 2:
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
    if (len(log_in_file) >= 5 and log_in_file[-5:] == '.html') or (
            len(log_in_file) >= 4 and log_in_file[-4:] == '.htm'):
        data = sorted(json.loads('[' + _get_log_values(log_in_file) + ']'), key=lambda x: sorted(x.keys()))
        # if user want a graph
        _graph = ''
        if graph_flag is not None:
            _graph = build_graph(graph_flag, language, data, _HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION)
        from lib.html_log import _log_data
        _css = _log_data.css_1
        _table = _log_data.table_title.format(_graph, _css, _HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION, )

        for value in data:
            if compatible.version() is 2:
                _table += _log_data.table_items.format(value[_HOST.decode('utf8')], value[_USERNAME.decode('utf8')],
                                                  value[_PASSWORD.decode('utf8')],
                                                  value[_PORT.decode('utf8')], value[_TYPE.decode('utf8')],
                                                  value[_DESCRIPTION.decode('utf8')])
            else:
                _table += _log_data.table_items.format(value[_HOST], value[_USERNAME], value[_PASSWORD],
                                                  value[_PORT], value[_TYPE], value[_DESCRIPTION])
        _table += _log_data.table_end + messages(language, 93) \
            .format(compatible.__version__, compatible.__code_name__,
                    datetime.datetime.now())
        _table = _table.encode('utf8')
        save = open(log_in_file, 'w' if type(_table) == str else 'wb')
        save.write(_table)
        save.close()
    else:
        data = sorted(json.loads('[' + _get_log_values(log_in_file) + ']'))
        _table = texttable.Texttable()
        _table.add_rows([[_HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION]])
        for value in data:
            _table.add_rows([[_HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION],
                             [value[_HOST], value[_USERNAME], value[_PASSWORD], value[_PORT], value[_TYPE],
                              value[_DESCRIPTION]]])
        save = open(log_in_file, 'wb')
        save.write(_table.draw().encode('utf8') + '\n\n' +
                   messages(language, 93).format(compatible.__version__, compatible.__code_name__,
                                                 datetime.datetime.now()).encode('utf8') + '\n\n')
        save.close()
    return 0
