import supertopicsign


def main_handler(event, context):
    supertopic = supertopicsign.SuperTopicHandler()
    supertopic.form_user_cookie_dict()
    for username, cookie in supertopic.user_cookie_dict.items():
        user_follow_list = supertopic.get_follow_list(username)
        if supertopic.is_user_all_topic_signed(user_follow_list):
            supertopic.user_topic_list[username] = user_follow_list
            continue
        else:
            convert_sign_list = supertopic.form_sign_list(user_follow_list)
            after_signed_list = supertopic.do_sign(cookie, convert_sign_list)
            supertopic.update_user_topic_list(username, after_signed_list)

    if len(supertopic.user_cookie_dict) == 0:
        supertopic.notifier.do_notify({}, "No available user")

    if supertopic.is_all_user_signed():
        supertopic.notifier.do_notify(supertopic.user_topic_list, "")

main_handler('', '')