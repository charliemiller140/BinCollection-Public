from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response

sb = SkillBuilder()

# LaunchRequest Handler
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to Bin Collection. You can ask for rubbish, recycling, or garden waste dates."
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

# GetBinDatesIntent Handler
class GetBinDatesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GetBinDatesIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Your next rubbish collection is on Monday, 6 January and the recycling is on Saturday, 11 January.Today's date is January 06"
        return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

# Register handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetBinDatesIntentHandler())

# Lambda Handler
lambda_handler = sb.lambda_handler()
