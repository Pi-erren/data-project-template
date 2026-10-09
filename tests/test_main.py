from src.main import main


def test_main(capsys):
    main()
    assert "Hello" in capsys.readouterr().out
