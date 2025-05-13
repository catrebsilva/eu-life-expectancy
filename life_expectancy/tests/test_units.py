import pandas as pd
from life_expectancy.cleaning import load_data
from life_expectancy.cleaning import clean_data
from life_expectancy.cleaning import save_data
from unittest.mock import patch

def test_load_data_returns_dataframe():
    """Verifica se a função load_data devolve um DataFrame com dados."""
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_clean_data_filters_region_and_cleans():
    """Verifica se a função clean_data filtra por região e limpa os dados corretamente."""

    # Arrange: criamos um mini DataFrame semelhante ao ficheiro real
    raw_data = pd.DataFrame({
        "unit,sex,age,geo\\time": ["YR,LIFE,0,PT", "YR,LIFE,0,FR", "YR,LIFE,0,PT"],
        "2019": ["82.5", "80.1", "83.2"],
        "2020": ["82.0", "79.9", ": "]
    })

    # Act: aplicamos a função ao DataFrame
    result = clean_data(raw_data, region="PT")

    # Assert: verificamos se o resultado está correto
    assert not result.empty
    assert all(result["region"] == "PT")
    assert set(result.columns) == {"unit", "sex", "age", "region", "year", "value"}

def test_save_data_calls_to_csv_with_correct_filename():
    """Verifica se save_data chama to_csv com o nome de ficheiro correto, sem escrever ficheiros reais."""

    # Criamos um DataFrame simples de exemplo
    df = pd.DataFrame({"col1": [1], "col2": [2]})

    # Simulamos a função to_csv para impedir escrita no disco
    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        save_data(df, region="PT")

        # Verificamos se a função foi chamada uma vez
        assert mock_to_csv.call_count == 1

        # Extraímos o argumento do caminho para ver se o nome do ficheiro está correto
        args, kwargs = mock_to_csv.call_args
        assert str(args[0]).endswith("pt_life_expectancy.csv")
