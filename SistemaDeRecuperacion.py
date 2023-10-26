import scrap
import process_script
import pandas as pd
from ModeloProbabilisticoFunciones import get_result
class SistemaDeRecuperacion:
    def __init__(self) -> None:
        ####### SCRAP
        scrap.scrap() # da el items.json
        ######## Process Text
        process_script.main() # da el tf.csv
        self.boolean_matrix = pd.read_csv('tf.csv')

    def query(self, query='none'):
        return get_result(query_raw=query, boolean_matrix=self.boolean_matrix)

if __name__ == "__main__":
    sistema = SistemaDeRecuperacion()
    result = sistema.query('André Paul Guillaume Gide was a French author and winner of the Nobel Prize in literature in 1947. Gides career ranged from its beginnings in the symbolist movement, to the advent of anticolonialism between the two World Wars.Known for his fiction as w')
    print(result)
