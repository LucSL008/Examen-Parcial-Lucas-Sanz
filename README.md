Para este codigo he usuado estructuras de datos como por ejemplo los heaps para dijkstra, sets para las estaciones visitadas, diccionarios para las distancias y una lista de adyacencias para el grafo.
Los heaps en dijkstra sobre todo para hacer operaciones, los sets para los visitados para que no haya repetidos, diciconario para distancias ya que para una estacion (o etiqueta) hay varias otras estaciones con un tiempo asociado
Una lista de adyacencias para el grafo para tener mas facil acceso.
Las complejidades temporales son O(1) para añadir estacion/conexion, O(n log n) para dijkstra, O(n) para DFS, O(n^2) para BFS.
Las espaciales son O(n) para el grafo, dijkstra y BFS/DFS por igual.
Me hubiera gustado cambiar el hecho de que para BFS he usado .pop(0) que altera toda la lista en lugar de deque, usando colas FIFO.
