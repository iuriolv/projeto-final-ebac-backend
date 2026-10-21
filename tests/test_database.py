from unittest.mock import MagicMock, patch
from app.database import get_db

def test_get_db_fecha_sessao():
    sessao_falsa = MagicMock()

    with patch("app.database.SessionLocal", return_value=sessao_falsa):
        gerador = get_db()
        sessao = next(gerador)

        assert sessao is sessao_falsa

        gerador.close()

        sessao_falsa.close.assert_called_once()