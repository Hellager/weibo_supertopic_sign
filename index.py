import supertopicsign


def main_handler(event, context):
    supertopic = supertopicsign.SuperTopicHandler()
    follow_list = supertopic.get_follow_list()
    supertopic.do_sign(supertopic.form_sign_list(follow_list))


main_handler('', '')