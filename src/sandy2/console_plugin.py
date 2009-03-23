from sandy2.common.parsing import IMicroParser, IMessageAction, Parser
from sandy2.common.plugins import IPlugin

class ConsolePlugin(IPlugin):
    
    def __init__(self, parser=None):
        self.parser=parser
        pass
    
    def start_up(self):
        self.parser.add_micro_parser(ConsoleUserFinder())
        self.parser.add_micro_parser(ConsoleOutputSetter())
        
        self.parser.add_action(ConsoleOutputReply())
    
    def run(self):
        print "Sandy console. Try 'help' to inspect what words I understand available."
        input = None
        while (True):
            input = raw_input('>> ')
            if input.strip() in ['exit', 'quit']:
                print "Bye"
                return
            self.do_command(input)

    def do_command(self, message):
        metadata = self.parser.parse({"incoming_message": message, "input_medium": "stdin", "tz_offset" : 0})
        self.parser.perform_actions(metadata)
        return metadata



class ConsoleUserFinder(IMicroParser):

    """Consumes: input_medium
    Produces: user
    """
    def __init__(self):
        self.is_preceeded_by = ['input_medium']
        self.is_followed_by = ['user_id']

    def micro_parse(self, metadata):
        if metadata.setdefault('input_medium', 'stdin') == 'stdin':
            import os
            username = os.getenv("USERNAME", "unknown user")
            metadata['fullname'] = username
            # not really necessary if we don't use the db.
            metadata['console_id'] = username
            metadata['user_id'] = -1

class ConsoleOutputSetter(IMicroParser):

    """Consumes: input_medium
    Produces: reply_medium
    """

    def __init__(self):
        #self.is_preceeded_by = ['input_medium']
        self.is_followed_by = ['reply_medium', 'reminder_medium']
        

    def micro_parse(self, metadata):
        if metadata.setdefault('input_medium', 'stdin') == 'stdin':
            metadata.setdefault('reply_medium', 'stdout')
            metadata.setdefault('reminder_medium', 'stdout')

class ConsoleOutputReply(IMessageAction):
    def perform_action(self, parser, metadata):        
        medium = metadata['output_medium']
        if medium == 'stdout':
            message = metadata['output_message']
            print message
            
