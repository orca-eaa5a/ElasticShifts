class Ransomspector(object):
    def __init__(self, traditional=True, verbose=False) -> None:
        self.traditional = traditional
        self.verbose = verbose
        self.filename_map_queue = {}
        self.newly_created_map_queue = {}
        self.rename_tracking_map = {}
        self.traditional_detection_patterns = {
            'main': [
                ('open', 'read', 'open', 'write'),
                ('open', 'read', 'write', 'rename'),
                ('open', 'read', 'write', 'open', 'rename'),
                ('open', 'read', 'write', 'open', 'read', 'rename'),
                ('open', 'read', 'write', 'open', 'read', 'open', 'rename'),
                ('open', 'read', 'open', 'write', 'open', 'rename'),
                ('open', 'read', 'open', 'rename', 'open', 'write'),
                ('open', 'rename', 'open', 'read', 'write'), # added patterns
                ('open', 'rename', 'read', 'write'), # added patterns
                ('open', 'rename', 'open', 'read', 'open', 'write'), # added patterns
                ('open', 'read', 'open', 'delete'),
                ('open', 'read', 'delete'),
            ],
            'sub': [
                ('create', 'write'),
                ('create', 'open', 'write'),
            ],
            'subrel': 10
        }
        self.renew_detection_patterns = {
            'main': [
                ('open', 'read', 'open', 'overwrite'),
                ('open', 'read', 'overwrite', 'rename'),
                ('open', 'read', 'overwrite', 'open', 'rename'),
                ('open', 'read', 'truncate', 'overwrite', 'open', 'rename'),
                ('open', 'read', 'open', 'overwrite', 'open', 'rename'),
                ('open', 'read', 'overwrite', 'open', 'read', 'rename'),
                ('open', 'read', 'overwrite', 'open', 'read', 'open', 'rename'),
                ('open', 'read', 'open', 'rename', 'open', 'overwrite'),
                ('open', 'rename', 'open', 'read', 'overwrite'), # added patterns
                ('open', 'rename', 'read', 'overwrite'), # added patterns
                ('open', 'rename', 'open', 'read', 'open', 'overwrite'), # added patterns
                ('open', 'read', 'open', 'delete'),
                ('open', 'read', 'delete'),
                ('open', 'read', 'open', 'truncate'),
                ('open', 'read', 'truncate'),
            ],
            'sub': [
                ('create', 'overwrite'),
                ('create', 'open', 'overwrite'),
            ],
            'subrel': 11
        }

    def in_queue(self, filename, operation):
        filename = self.get_origin_name(filename)

        if not self.traditional and operation == "append":
            return True # jump

        if operation == "create":
            self.newly_created_map_queue[filename] = FSequence()
        
        if filename in self.newly_created_map_queue:
            return self.newly_created_map_queue[filename].push(operation)

        if not filename in self.filename_map_queue:
            self.filename_map_queue[filename] = FSequence()

        return self.filename_map_queue[filename].push(operation)