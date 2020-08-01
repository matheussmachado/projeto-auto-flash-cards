import shelve

def text_source_reset(source: str, source_before: list) -> None:
    """
        Função que realiza o reset do arquivo de texto que serve para fonte de criação nos testes automatizados.

        Args:
            source (str): path do arquivo de texto.
            source_before (list): lista contendo o conteúdo anterior do arquivo passado, antes de ser submetido aos testes."""
    with open(source, "w") as src:
        for phrse in source_before:
            src.write(f"{phrse}\n")


def db_cards_reset(source: str, key: str, source_before: list) -> None:
    """
        Método que realiza o reset da estrutura de persistência após submetida aos testes automatizados.

        Args:
            source (str): path do arquivo da estrutura de db.
            key (str): chave/coluna que aloca a lista dos objetos MyCard criados em produção.
            source_before (list): lista da estrutura antes da submissão dos testes automatizados."""
    with shelve.open(source) as db:
        db[key] = source_before