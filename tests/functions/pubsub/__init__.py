from gcloud_functions_utils.parsers.trigger.pubsub import EventParser


def basic_print_event(event, context):
    print(event, end="")


def parser_print_event_data(event, context):
    parsed_event = EventParser(event)
    print(parsed_event.data, end="")


def parser_print_event_attributes(event, context):
    parsed_event = EventParser(event)
    print(parsed_event.attributes, end="")
