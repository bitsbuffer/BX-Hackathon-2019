from utils import listdir_full_path, fetch_null_response_node
from page_diff import get_page_number_diffs, get_pages
from annotations import are_annotations_present, list_annotations_present
from signature_detection import is_signature_present
from markup_detection  import is_markup_present
import json
import os


def do_the_thing(src_dir):
    """
    Driver function
    :param src_dir: Source Directory which contains all files
    :return: Json response with all data
    """

    files_to_read = listdir_full_path(src_dir)

    files_to_read = [file for file in files_to_read if file.endswith('.pdf')]

    if len(files_to_read) == 0:
        return fetch_null_response_node("No file found")

    files_to_read.sort()

    page_count = get_pages(files_to_read)
    page_diff_flag = get_page_number_diffs(files_to_read)
    annotations_list = list_annotations_present(files_to_read)
    annotations_flag = are_annotations_present(files_to_read)
    signature_detected = is_signature_present(files_to_read)
    markup_present = is_markup_present(files_to_read)
    response = dict()

    for file in files_to_read:
        file_dict = dict()
        file_name = os.path.basename(file)
        file_dict["page_count"] = page_count[file_name]
        file_dict["page_diff_flag"] = page_diff_flag[file_name]
        file_dict["annotations_list"] = annotations_list[file_name]
        file_dict["annotations_flag"] = annotations_flag[file_name]
        file_dict["signature_present"] = signature_detected[file_name]
        file_dict["markup_present"] = markup_present[file_name]

        flag = page_diff_flag[file_name]

        if page_diff_flag[file_name] not in (True, False):
            flag = False

        if flag and annotations_flag[file_name] and markup_present[file_name]:
            file_dict["send_through"] = True
        else:
            file_dict["send_through"] = False

        response[file_name] = file_dict

    # pprint.pprint(json.dumps(response))
    return response

    # print('____________________________________________')
    # print("***********Page Diffs***********")
    # pprint.pprint(get_page_number_diffs(files_to_read))

    # print('____________________________________________')
    # print("***********Annotations***********")
    # pprint.pprint(are_annotations_present(files_to_read))

    # print('____________________________________________')
    # print("***********List Annotations***********")
    # pprint.pprint(list_annotations_present(files_to_read))
