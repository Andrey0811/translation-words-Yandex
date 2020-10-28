import requests as req
import json as j
from docx import Document


def get_words(file_name: str) -> list:
    with open(file_name, 'r') as f:
        words = [i.strip() for i in f.readlines()]
    return words


def get_request(data: dict, headers: dict,
                link='https://translate.api.cloud.yandex.net/translate/v2/translate') -> req.Response:
    return req.post(link, headers=headers, data=j.dumps(data))


def prepare_headers(token: str) -> dict:
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }


def prepare_data(folder_id: str, words: list, translate_lan='ru') -> dict:
    return {
        'folder_id': f'{folder_id}',
        'texts': words,
        'targetLanguageCode': translate_lan
    }


def get_iam_token(o_auth_token: str) -> str:
    data: req.Response = req.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
                                  data='{"yandexPassportOauthToken": "' + o_auth_token + '"}')
    return j.loads(data.text)['iamToken']


def get_secret_tokens(file_name) -> tuple:
    with open(file_name, 'r') as f:
        data = j.loads(f.read())
    return data['o_auth'], data['folder_id']


def get_translate_word(resp: req.Response) -> list:
    data = j.loads(resp.text)
    temp = []

    for i in data['translations']:
        temp.append(i['text'])

    return temp


def words_with_translation() -> dict:
    o_auth, folder_id = get_secret_tokens('yandex_cloud.json')
    i_am_token = get_iam_token(o_auth)
    words = get_words('words.txt')
    resp = get_request(prepare_data(folder_id, words), prepare_headers(i_am_token))
    translate_words = get_translate_word(resp)
    return dict(zip(words, translate_words))


def get_document(words: dict, file_name='dictionary.docx'):
    doc = Document()
    table = doc.add_table(rows=len(words), cols=4)
    table.style = 'Table Grid'

    idx = 0
    for word, translate in words.items():
        table.rows[idx].cells[0].width = 0.5
        table.rows[idx].cells[0].text = str(idx + 1)
        table.rows[idx].cells[1].text = word
        table.rows[idx].cells[2].text = translate
        idx += 1

    doc.add_page_break()
    if not file_name.endswith('.docx'):
        file_name += '.docx'
    doc.save(file_name)


def main():
    get_document(words_with_translation())


main()


