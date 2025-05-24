class OnlineRanker(object):
    def __init__(self, traditional=True, verbose=False) -> None:
        self.kellect = mock_kellect.Kellect()
        self.traditional=traditional
        self.verbose = verbose
        self.filekey_name_map = {}
        self.filekey_sequence_map = {}
        self.newfilekey_sequence_map = {}
        self.traditional_detection_patterns = {
            'main': [
                ('read', 'write', 'rename'),
                ('read', 'write', 'read', 'rename'),
                ('read', 'rename', 'write'),
                ('rename', 'read', 'write'),
                ('read', 'delete'),
            ],
            'sub': [
                ('fileCreate', 'write'),
                ('fileCreate', 'write', 'rename'),
                ('fileCreate', 'open', 'overwrite'),
                ('fileCreate', 'open', 'overwrite', 'rename'),
            ],
            'subrel': 4
        }
        self.renew_detection_patterns = {
            'main': [
                ('read', 'overwrite', 'rename'),
                ('read', 'overwrite', 'read', 'rename'),
                ('read', 'truncate', 'overwrite', 'rename'),
                ('read', 'rename', 'overwrite'),
                ('rename', 'read', 'overwrite'),
                ('read', 'delete'),
                ('read', 'truncate'),
            ],
            'sub': [
                ('fileCreate', 'overwrite'),
                ('fileCreate', 'overwrite', 'rename'),
                ('fileCreate', 'open', 'overwrite'),
                ('fileCreate', 'open', 'overwrite', 'rename'),
            ],
            'subrel': 5
        }
        pass