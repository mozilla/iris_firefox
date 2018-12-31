from iris2.core.arg_parser import parse_args


class Plugin:

    def pytest_sessionstart(self, session):
        print('\n\n** Test session {} started **\n'.format(session.name))
        print('\nIris settings: \n')
        settings_list = []
        args = parse_args()
        for arg in vars(args):
            settings_list.append('{}: {}'.format(arg, getattr(args, arg)))
        print(', '.join(settings_list))
        print('\n')

    def pytest_sessionfinish(self, session):
        print("\n\n** Test session {} complete **\n".format(session.name))

    def pytest_runtestloop(self, session):
        pass
        # print('RUN TEST LOOP')

    def pytest_runtest_logstart(self, nodeid, location):
        pass

    def pytest_runtest_call(self, item):
        pass
        # print('Executing: [{}]'.format(item.parent.parent.name))

    def pytest_runtest_logfinish(self, nodeid, location):
        pass


def reason_for_failure(report):
    if report.outcome == 'passed':
        return ''
    else:
        return report.longreprtext
