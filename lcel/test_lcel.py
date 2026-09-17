from index import parse_numbered_subquestions


def test_maximum_three_subquestions():
    text = """
    1. What is Node.js?
    2. How does Node.js handle requests?
    3. How can Node.js performance be improved?
    4. What are Node.js alternatives?
    """

    result = parse_numbered_subquestions(text)

    assert len(result) <= 3