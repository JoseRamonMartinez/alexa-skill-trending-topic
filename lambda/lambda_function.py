from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_s3.adapter import S3Adapter
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.skill_builder import CustomSkillBuilder
from dotenv import load_dotenv

import logging
import json
import random
import os

from controllers.trends import trends
from controllers.popular_topic_tweets import popular_topic_tweets

s3_adapter = S3Adapter(bucket_name = os.environ.get("S3_PERSISTENCE_BUCKET"))

# Initializing the logger and setting the level to "INFO"
# Read more about it here https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Intent Handlers

# This handler responds when required environment variables are missing
class InvalidConfigHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        request_attributes = handler_input.attributes_manager.request_attributes
        invalid_config = request_attributes["invalid_config"]
        return invalid_config
        
    def handle(self,handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = language_prompts["ENV_NOT_CONFIGURED"]
        return ( 
            handler_input.response_builder
                .speak(speech_output)
                .response 
            )

#This Handler is called when the skill is invoked by using only the invocation name(Ex. Alexa, open tendencias de twitter)
class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        skill_name = language_prompts["SKILL_NAME"]
        speech_output = random.choice(language_prompts["WELCOME"]).format(skill_name)
        reprompt = random.choice(language_prompts["ASK"])
        return (
            handler_input.response_builder
                .speak(speech_output+reprompt)
                .ask(reprompt)
                .set_card(SimpleCard(skill_name,speech_output))
                .response
            )

class PlayTrendsCountryHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PlayTrendsCountry")(handler_input)
    
    def handle(self,handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        skill_name = language_prompts["SKILL_NAME"]
        country = handler_input.request_envelope.request.intent.slots["country"].slot_value.value
        trends_list=trends(country)
        
        speech_output = random.choice(language_prompts["COUNTRY_TRENDS"]).format(country)
        for i in range(0,10):
            speech_output+=f'{i+1}, {trends_list[i]}. '
        reprompt = random.choice(language_prompts["ASK_MORE"])
        
        return(
            handler_input.response_builder
                .speak(speech_output+reprompt)
                .ask(reprompt)
                .set_card(SimpleCard(skill_name,speech_output))
                .response
            )

class PlayPopularTopicTweetsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PlayPopularTopicTweets")(handler_input)
    
    def handle(self,handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        skill_name = language_prompts["SKILL_NAME"]
        topic = handler_input.request_envelope.request.intent.slots["topic"].slot_value.value
        
        language_request= str(handler_input.request_envelope.request.locale[:2])

        topic_tweets=popular_topic_tweets(topic, language_request).copy()
        speech_output = random.choice(language_prompts["TOPIC_TWEETS"]).format(topic)
        for i in topic_tweets: 
            speech_output+= f'{i} {random.choice(language_prompts["SAY"])}; {topic_tweets[i]}. '
        reprompt = random.choice(language_prompts["ASK_MORE"])
        return(
            handler_input.response_builder
                .speak(speech_output+reprompt)
                .ask(reprompt)
                .set_card(SimpleCard(skill_name,speech_output))
                .response
            )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["CANCEL_STOP_RESPONSE"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["HELP"])
        reprompt = random.choice(language_prompts["HELP_REPROMPT"])
        ask = random.choice(language_prompts["ASK"])

        return (
            handler_input.response_builder
                .speak(speech_output+ask)
                .ask(reprompt)
                .response
            )

# This handler is used to handle the AMAZON.RepeatIntent. It lets users ask Alexa to repeat the last thing that was said.
class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        
        repeat_speech_output = session_attributes["repeat_speech_output"]
        repeat_reprompt = session_attributes["repeat_reprompt"]
        
        speech_output = random.choice(language_prompts["REPEAT"]).format(repeat_speech_output)
        reprompt = random.choice(language_prompts["REPEAT_REPROMPT"]).format(repeat_reprompt)
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# This handler handles utterances that can't be matched to any other intent handler.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["FALLBACK"])
        reprompt = random.choice(language_prompts["FALLBACK_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class SessionEndedRequesthandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with the reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Exception Handlers

# This exception handler handles syntax or routing errors. If you receive an error stating 
# the request handler is not found, you have not implemented a handler for the intent or 
# included it in the skill builder below
class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = language_prompts["ERROR"]
        reprompt = language_prompts["ERROR_REPROMPT"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# Interceptors

# This interceptor checks if the environment variable file is setup in the right way
class InvalidConfigInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        try:
            load_dotenv()
            env_variable_1 = os.environ['CONSUMER_KEY']
            env_variable_2 = os.environ['CONSUMER_SECRET']
            handler_input.attributes_manager.request_attributes["invalid_config"] = False
        except:
            handler_input.attributes_manager.request_attributes["invalid_config"] = True

# This interceptor logs each request sent from Alexa to our endpoint.
class RequestLogger(AbstractRequestInterceptor):

    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

# This interceptor logs each response our endpoint sends back to Alexa.
class ResponseLogger(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

# This interceptor is used for supporting different languages and locales. It detects the users locale,
# loads the corresponding language prompts and sends them as a request attribute object to the handler functions.
class LocalizationInterceptor(AbstractRequestInterceptor):

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        
        try:
            with open("languages/"+str(locale)+".json") as language_data:
                language_prompts = json.load(language_data)
        except:
            with open("languages/"+ str(locale[:2]) +".json") as language_data:
                language_prompts = json.load(language_data)
        
        handler_input.attributes_manager.request_attributes["_"] = language_prompts

# This interceptor fetches the speech_output and reprompt messages from the response and pass them as
# session attributes to be used by the repeat intent handler later on.
class RepeatInterceptor(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["repeat_speech_output"] = response.output_speech.ssml.replace("<speak>","").replace("</speak>","")
        try:
            session_attributes["repeat_reprompt"] = response.reprompt.output_speech.ssml.replace("<speak>","").replace("</speak>","")
        except:
            session_attributes["repeat_reprompt"] = response.output_speech.ssml.replace("<speak>","").replace("</speak>","")


# Skill Builder
# Define a skill builder instance and add all the request handlers,
# exception handlers and interceptors to it.

sb = CustomSkillBuilder (persistence_adapter = s3_adapter)
sb.add_request_handler(InvalidConfigHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PlayTrendsCountryHandler())
sb.add_request_handler(PlayPopularTopicTweetsHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequesthandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(InvalidConfigInterceptor())
sb.add_global_response_interceptor(RepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()