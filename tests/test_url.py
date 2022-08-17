'''``include`` directive tests.'''

import pytest

from mkdocs_include_markdown_plugin.event import on_page_markdown


@pytest.mark.parametrize(
    (
        'includer_schema',
        'url_to_include',
        'expected_result',
    ),
    (
        pytest.param(
            '# Header\n\n{% include "{url}" %}\n',
            'https://pastebin.com/raw/NZwqqTtf',
            '# Header\n\nremote content\n',
            id='remote-content',
        ),
    ),
)
def test_url(
    includer_schema,
    url_to_include,
    expected_result,
    page,
    caplog,
    tmp_path,
):
    includer_filepath = tmp_path / 'includer.md'

    # assert content
    page_content = includer_schema.replace(
        '{url}', url_to_include,
    )
    includer_filepath.write_text(page_content)

    assert (
        on_page_markdown(
            page_content,
            page(includer_filepath),
            tmp_path,
        )
        == expected_result
    )

    assert len(caplog.records) == 0
