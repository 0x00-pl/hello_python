import json
import os.path
from os.path import join

__author__ = 'pl'


def lexer(text):
    s_code, s_string, s_comment = range(3)
    token = ""
    state = s_code
    comment_level = 0

    for c in text:
        token += c
        if state == s_code:
            if token.endswith('"'):
                yield token[:-1]
                state, token = s_string, '"'
            elif token.endswith('(*'):
                yield token[:-2]
                state, token, comment_level = s_comment, '(*', 1
            else:
                pass
        elif state == s_string:
            if token.replace('""', '').endswith('"'):
                yield token
                state, token = s_code, ''
        elif state == s_comment:
            if token.endswith("(*"):
                comment_level += 1
            elif token.endswith("*)"):
                comment_level -= 1
                if comment_level < 0:
                    raise ValueError()
            else:
                pass
            if comment_level == 0:
                yield token
                state, token = s_code, ''
        else:
            raise NotImplementedError()
    yield token


def make_element(state, index, origin_text, trans_text, info):
    return {'state': state, 'index': index, 'origin': origin_text, 'trans': trans_text, 'info': info}


def make_elements(tokens, old_element_dict):
    old_element_remind = dict(old_element_dict)
    for i, text in zip(range(999999), tokens):
        if not text.startswith('(*'):
            continue
        old_element = old_element_dict.get(text, None)
        old_element_remind.pop(text, None) if old_element is not None else None
        if old_element is None:
            yield make_element('TODO', i, text, text, {})
        else:
            yield make_element(old_element['state'], i, text, old_element['trans'], old_element['info'])
    for i in old_element_remind.values():
        i['state'] = 'UNUSED'
        yield i


def make_element_json(element):
    return """
{{"index": {}, "state": {},
  "origin": {},
  "trans": {},
  "info": {}
}}""".format(int(element['index']),
             json.dumps(element['state']),
             json.dumps(element['origin']),
             json.dumps(element['trans']),
             json.dumps(element['info']))


def make_elements_json(tokens, old_element_dict):
    element_json_list = [make_element_json(element) for element
                         in make_elements(tokens, old_element_dict)]
    return '[' + ','.join(element_json_list) + ']'


def make_element_dict(elements):
    ret = {}
    for element in elements:
        ret[element['origin']] = element

    return ret


def read_elements_dict(json_str):
    elements = json.loads(json_str)
    return make_element_dict(elements)


def apply_element_dict(origin_text, element_dict):
    ret_text = ""
    total_comment_count = 0
    translated_count = 0
    for tok in lexer(origin_text):
        if tok.startswith('(*'):
            total_comment_count += 1
            element = element_dict.get(tok)
            if element is None:
                ret_text += tok
            elif element['state'] != 'DONE':
                ret_text += tok
            else:
                translated_count += 1
                ret_text += element['trans']
        else:
            ret_text += tok
    return (translated_count, total_comment_count), ret_text


def make_element_json_file(origin_filename, output_filename):
    old_element_dict = {}
    if os.path.isfile(output_filename):
        with open(output_filename, 'r') as old_file:
            old_element_json = old_file.read()
            old_element_dict = make_element_dict(json.loads(old_element_json))

    with open(origin_filename, 'r') as origin_file:
        origin_str = origin_file.read()

    output_str = make_elements_json([t for t in lexer(origin_str)], old_element_dict)
    with open(output_filename, 'w') as output_file:
        output_file.write(output_str)


def apply_element_dict_file(origin_filename, json_filename, output_filename):
    with open(origin_filename, 'r') as origin_file, \
            open(json_filename, 'r') as json_file, \
            open(output_filename, 'w') as output_file:
        origin_str = origin_file.read()
        element_dict = read_elements_dict(json_file.read())
        counters, output_str = apply_element_dict(origin_str, element_dict)

        output_file.write(output_str)
    return counters


def change_first_dir(input_file_path, dest_path):
    old_root, path = input_file_path.split(os.sep, 1)
    new_path = os.path.join(dest_path, path)
    return new_path


def process_v_file(old_path):
    print(old_path, ':', end=' ... ')
    json_path = change_first_dir(old_path, 'trans') + '.json'
    new_path = change_first_dir(old_path, 'SFCTSource.cn')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    os.makedirs(os.path.dirname(new_path), exist_ok=True)
    make_element_json_file(old_path, json_path)
    done_num, total_num = apply_element_dict_file(old_path, json_path, new_path)
    print(int(done_num / total_num * 100), '%', '({}/{})'.format(done_num, total_num))
    return done_num == total_num


def walk_all_v_file(base_path):
    for root, dirs, files in os.walk(base_path):
        for file_name in files:
            if file_name.endswith('.v'):
                file_full_path = os.path.join(root, file_name)
                yield file_full_path


def progress_all():
    total_num, finished_num = 0, 0
    for p in walk_all_v_file('SFCTSource'):
        finished = process_v_file(p)
        total_num += 1
        finished_num += 1 if finished else 0
    print('total:', int(finished_num / total_num * 100), '%', '({}/{})'.format(finished_num, total_num))


def main():
    progress_all()
    return

if __name__ == '__main__':
    main()
