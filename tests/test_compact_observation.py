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
    assert "Link A" in obs.links
    assert "Click Me" in obs.buttons
    assert "query" in obs.inputs
    assert "Hello World" in obs.text_snippet
