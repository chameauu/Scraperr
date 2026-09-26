from scraper.observation import build_compact_observation


def test_compact_observation_extracts_text_and_elements():
    html = """
    <html><head><title>Example</title></head>
    <body>
      <a href="/a">Link A</a>
      <button>Click Me</button>
      <input id="q" name="query" />
      <p>Hello World</p>
    </body></html>
    """
    obs = build_compact_observation(html, max_text=50)

    assert obs.title == "Example"
    assert any(link["label"] == "Link A" for link in obs.links)
    assert any(button["label"] == "Click Me" for button in obs.buttons)
    assert any(item["name"] == "query" for item in obs.inputs)
    assert "Hello World" in obs.text_snippet


def test_compact_observation_builds_deterministic_selectors():
    html = """
    <html><body>
      <a href="/a" id="link-id">Link A</a>
      <a href="/b" aria-label="Link B"></a>
      <button data-testid="submit-btn">Submit</button>
      <input name="query" />
    </body></html>
    """
    obs = build_compact_observation(html, max_text=50)

    assert any(link["selector"] == "a#link-id" for link in obs.links)
    assert any(link["selector"] == 'a[aria-label="Link B"]' for link in obs.links)
    assert any(button["selector"] == 'button[data-testid="submit-btn"]' for button in obs.buttons)
    assert any(item["selector"] == 'input[name="query"]' for item in obs.inputs)
