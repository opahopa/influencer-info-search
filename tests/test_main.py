from main import check_proxylist_countries

def test_check_countries():
    assert check_proxylist_countries() is True
