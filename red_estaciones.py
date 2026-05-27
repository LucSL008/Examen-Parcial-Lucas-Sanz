
import heapq
import json


class RedEstaciones:
    def __init__(self, archivo_datos="red_estaciones.json"):
        self.grafo = {}  # Lista de adyacencia: {estacion: {destino: tiempo}}
        self.archivo_datos = archivo_datos
        self.cargar_desde_archivo()
    
    # ==================== MÉTODOS DE CARGA Y GUARDADO ====================
    
    def cargar_desde_archivo(self):
        """Carga la red desde un archivo JSON"""
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.grafo = datos
                print(f"✓ Red cargada desde {self.archivo_datos}")
                print(f"  Estaciones: {len(self.grafo)}")
        except FileNotFoundError:
            print(f"  Archivo {self.archivo_datos} no encontrado. Red vacía creada.")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON. Iniciando con red vacía.")
            self.grafo = {}
        except Exception as e:
            print(f"Error al cargar archivo: {e}")
            self.grafo = {}
    
    def cargar_desde_json(self, archivo_json):
        """
        Carga la red desde archivo JSON (formato: lista de objetos con origen, destino, minutos)
        
        Args:
            archivo_json: Ruta del archivo JSON
        """
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            conexiones_cargadas = 0
            
            # Si es una lista de objetos
            if isinstance(datos, list):
                for idx, item in enumerate(datos, 1):
                    try:
                        if not isinstance(item, dict):
                            print(f"  ⚠ Elemento {idx}: debe ser un objeto JSON")
                            continue
                        
                        origen = item.get('origen', '').strip()
                        destino = item.get('destino', '').strip()
                        tiempo = item.get('minutos')
                        
                        if not origen or not destino:
                            print(f"  ⚠ Elemento {idx}: falta 'origen' o 'destino'")
                            continue
                        
                        if not isinstance(tiempo, int):
                            print(f"  ⚠ Elemento {idx}: 'minutos' debe ser un número entero")
                            continue
                        
                        self.anadir_conexion(origen, destino, tiempo, mostrar_msg=False)
                        conexiones_cargadas += 1
                    except Exception as e:
                        print(f"  ⚠ Error al procesar elemento {idx}: {e}")
            else:
                print(f"✗ Formato JSON inválido: debe ser una lista de objetos")
                return
            
            print(f"✓ Cargadas {conexiones_cargadas} conexiones desde {archivo_json}")
            self.guardar_en_archivo()
        
        except FileNotFoundError:
            print(f"✗ Archivo '{archivo_json}' no encontrado")
        except json.JSONDecodeError as e:
            print(f"✗ Error al decodificar JSON: {e}")
        except Exception as e:
            print(f"✗ Error al cargar JSON: {e}")
    
    def guardar_en_archivo(self):
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(self.grafo, f, indent=2, ensure_ascii=False)
            print(f"✓ Red guardada en {self.archivo_datos}")
        except Exception as e:
            print(f"✗ Error al guardar: {e}")
    
    def anadir_estacion(self, nombre_estacion):
        """
        Añade una estación a la red
        
        Args:
            nombre_estacion: Nombre de la estación
            
        Returns:
            True si se añadió, False si ya existía
        """
        try:
            if not nombre_estacion or not isinstance(nombre_estacion, str):
                print("✗ El nombre de la estación debe ser una cadena no vacía")
                return False
            
            nombre_estacion = nombre_estacion.strip()
            
            if nombre_estacion in self.grafo:
                print(f"⚠ La estación '{nombre_estacion}' ya existe")
                return False
            
            self.grafo[nombre_estacion] = {}
            print(f"✓ Estación '{nombre_estacion}' añadida")
            self.guardar_en_archivo()
            return True
        
        except Exception as e:
            print(f"Error al añadir estación: {e}")
            return False
    
    def anadir_conexion(self, origen, destino, tiempo, mostrar_msg=True):
        #Alguna manera de hacer que cuando añades estacion/conexion se ponga en el json
        """
        Añade una conexión entre dos estaciones
        
        Args:
            origen: Estación de origen
            destino: Estación de destino
            tiempo: Tiempo en minutos (debe ser positivo)
            mostrar_msg: Si mostrar mensaje de confirmación
            
        Returns:
            True si se añadió, False si hubo error
        """
        try:
            # Validaciones
            if tiempo <= 0:
                print(f"✗ El tiempo debe ser positivo (recibido: {tiempo})")
                return False
            
            if not isinstance(tiempo, int):
                print(f"✗ El tiempo debe ser un número entero")
                return False
            
            origen = origen.strip()
            destino = destino.strip()
            
            if origen == destino:
                print(f"✗ No se pueden conectar estaciones consigo mismas")
                return False
            
            # Crear estaciones si no existen
            if origen not in self.grafo:
                self.grafo[origen] = {}
                if mostrar_msg:
                    print(f"  ℹ Estación '{origen}' creada automáticamente")
            
            if destino not in self.grafo:
                self.grafo[destino] = {}
                if mostrar_msg:
                    print(f"  ℹ Estación '{destino}' creada automáticamente")
            
            # Verificar conexión duplicada
            if destino in self.grafo[origen]:
                tiempo_anterior = self.grafo[origen][destino]
                print(f"⚠ Conexión {origen}→{destino} ya existe ({tiempo_anterior} min)")
                return False
            
            # Añadir conexión (grafo no dirigido)
            self.grafo[origen][destino] = tiempo
            self.grafo[destino][origen] = tiempo
            
            if mostrar_msg:
                print(f"✓ Conexión '{origen}' ↔ '{destino}': {tiempo} minutos")
                self.guardar_en_archivo()
            
            return True
        
        except Exception as e:
            print(f"✗ Error al añadir conexión: {e}")
            return False
    
    # ==================== MÉTODOS DE VISUALIZACIÓN ====================
    
    def mostrar_todas_estaciones(self):
        """Muestra todas las estaciones en la red"""
        if not self.grafo:
            print("  (Red vacía)")
            return
        
        print(f"\n{'ESTACIONES EN LA RED':^50}")
        print("=" * 50)
        for idx, estacion in enumerate(sorted(self.grafo.keys()), 1):
            num_conexiones = len(self.grafo[estacion])
            print(f"  {idx}. {estacion:<30} ({num_conexiones} conexiones)")
        print(f"\nTotal: {len(self.grafo)} estaciones")
    
    def mostrar_conexiones(self, estacion):
        """
        Muestra todas las conexiones directas de una estación
        
        Args:
            estacion: Nombre de la estación
        """
        try:
            estacion = estacion.strip()
            
            if estacion not in self.grafo:
                print(f"✗ La estación '{estacion}' no existe")
                return
            
            conexiones = self.grafo[estacion]
            
            if not conexiones:
                print(f"\nEstación '{estacion}': sin conexiones directas")
                return
            
            print(f"\n{'CONEXIONES DE ' + estacion:^50}")
            print("=" * 50)
            print(f"{'Destino':<30} {'Tiempo (min)':>15}")
            print("-" * 50)
            
            tiempo_total = 0
            for destino in sorted(conexiones.keys()):
                tiempo = conexiones[destino]
                tiempo_total += tiempo
                print(f"  {destino:<28} {tiempo:>15}")
            
            print("-" * 50)
            print(f"{'Total de conexiones:':<30} {len(conexiones):>15}")
            print(f"{'Tiempo promedio:':<30} {tiempo_total/len(conexiones):>15.1f}")
        
        except Exception as e:
            print(f"✗ Error al mostrar conexiones: {e}")
    
    # ==================== ALGORITMOS DE BÚSQUEDA ====================
    
    def dijkstra(self, origen, destino):
        try:
            origen = origen.strip()
            destino = destino.strip()
            
            if origen not in self.grafo:
                print(f"Estación origen '{origen}' no existe")
                return None, None
            
            if destino not in self.grafo:
                print(f"Estación destino '{destino}' no existe")
                return None, None
            
            if origen == destino:
                print("Ya estás en el destino")
                return [origen], 0
            
            distancias = {estacion: float('inf') for estacion in self.grafo}
            distancias[origen] = 0
            anteriores = {estacion: None for estacion in self.grafo}
            visitados = set()
            
            cola = [(0, origen)]
            
            while cola:
                distancia_actual, nodo_actual = heapq.heappop(cola)
                
                if nodo_actual in visitados:
                    continue
                
                visitados.add(nodo_actual)
                
                if nodo_actual == destino:
                    break
                
                if distancia_actual > distancias[nodo_actual]:
                    continue
                
                for vecino, peso in self.grafo[nodo_actual].items():
                    if vecino not in visitados:
                        nueva_distancia = distancia_actual + peso
                        
                        if nueva_distancia < distancias[vecino]:
                            distancias[vecino] = nueva_distancia
                            anteriores[vecino] = nodo_actual
                            heapq.heappush(cola, (nueva_distancia, vecino))
            
            if distancias[destino] == float('inf'):
                return None, None
            
            ruta = []
            nodo = destino
            while nodo is not None:
                ruta.append(nodo)
                nodo = anteriores[nodo]
            ruta.reverse()
            
            return ruta, distancias[destino]
        
        except Exception as e:
            print(f"Error en Dijkstra: {e}")
            return None, None
    
    def bfs(self, origen, destino):
        try:
            origen = origen.strip()
            destino = destino.strip()
            
            if origen not in self.grafo or destino not in self.grafo:
                return False
            
            if origen == destino:
                return True
            
            visitados = set()
            cola = [origen]
            visitados.add(origen)
            
            while cola:
                nodo_actual = cola.pop(0)
                
                for vecino in self.grafo[nodo_actual]:
                    if vecino == destino:
                        return True
                    
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append(vecino)
            
            return False
        
        except Exception as e:
            print(f"Error en BFS: {e}")
            return False
    
    def dfs(self, origen, destino):
        try:
            origen = origen.strip()
            destino = destino.strip()
            
            if origen not in self.grafo or destino not in self.grafo:
                return False
            
            visitados = set()
            
            def _dfs_recursivo(nodo):
                if nodo == destino:
                    return True
                
                visitados.add(nodo)
                
                for vecino in self.grafo[nodo]:
                    if vecino not in visitados:
                        if _dfs_recursivo(vecino):
                            return True
                
                return False
            
            return _dfs_recursivo(origen)
        
        except Exception as e:
            print(f"Error en DFS: {e}")
            return False
    
    # ==================== MÉTODOS DE ANÁLISIS ====================
    
    def estadisticas(self):
        if not self.grafo:
            print("Red vacía")
            return
        
        num_estaciones = len(self.grafo)
        num_conexiones = sum(len(conexiones) for conexiones in self.grafo.values()) // 2
        
        tiempos = []
        for conexiones in self.grafo.values():
            tiempos.extend(conexiones.values())
        tiempos = [t for t in tiempos if t > 0]
        
        print(f"\n{'ESTADÍSTICAS DE LA RED':^50}")
        print("=" * 50)
        print(f"  Estaciones: {num_estaciones}")
        print(f"  Conexiones: {num_conexiones}")
        
        if tiempos:
            print(f"  Tiempo mínimo: {min(tiempos)} minutos")
            print(f"  Tiempo máximo: {max(tiempos)} minutos")
            print(f"  Tiempo promedio: {sum(tiempos)/len(tiempos):.1f} minutos")
        
        grados = [len(conexiones) for conexiones in self.grafo.values()]
        print(f"  Estación más conectada: {max(grados)} conexiones")
        print(f"  Estación menos conectada: {min(grados)} conexiones")


def menu_principal():
    red = RedEstaciones("red_estaciones.json")
    
    while True:
        print("\n" + "="*50)
        print("RED DE ESTACIONES - MENÚ PRINCIPAL".center(50))
        print("="*50)
        print("""
  1. Cargar red desde JSON
  2. Añadir estación
  3. Añadir conexión
  4. Ver todas las estaciones
  5. Ver conexiones de una estación
  6. Calcular ruta más rápida (Dijkstra)
  7. Verificar conectividad (BFS)
  8. Verificar conectividad (DFS)
  9. Estadísticas
  0. Salir
        """)
        
        opcion = input("Selecciona una opción: ").strip()
        
        try:
            if opcion == "1":
                red.cargar_desde_json("estaciones.json")
            
            elif opcion == "2":
                estacion = input("Nombre de la estación: ").strip()
                red.anadir_estacion(estacion)
            
            elif opcion == "3":
                origen = input("Estación origen: ").strip()
                destino = input("Estación destino: ").strip()
                try:
                    tiempo = int(input("Tiempo (minutos): ").strip())
                    red.anadir_conexion(origen, destino, tiempo)
                except ValueError:
                    print("✗ El tiempo debe ser un número entero")
            
            elif opcion == "4":
                red.mostrar_todas_estaciones()
            
            elif opcion == "5":
                estacion = input("Nombre de la estación: ").strip()
                red.mostrar_conexiones(estacion)
            
            elif opcion == "6":
                origen = input("Estación de partida: ").strip()
                destino = input("Estación de llegada: ").strip()
                ruta, tiempo = red.dijkstra(origen, destino)
                
                if ruta:
                    print(f"\n{'RUTA MÁS RÁPIDA':^50}")
                    print("="*50)
                    print(f"Recorrido: {' → '.join(ruta)}")
                    print(f"Tiempo total: {tiempo} minutos")
                else:
                    print(f"No hay ruta disponible entre '{origen}' y '{destino}'")
            
            elif opcion == "7":
                origen = input("Estación de partida: ").strip()
                destino = input("Estación de llegada: ").strip()
                if red.bfs(origen, destino):
                    print(f"Existe conexión entre '{origen}' y '{destino}' (BFS)")
                else:
                    print(f"No hay conexión entre '{origen}' y '{destino}' (BFS)")
            
            elif opcion == "8":
                origen = input("Estación de partida: ").strip()
                destino = input("Estación de llegada: ").strip()
                if red.dfs(origen, destino):
                    print(f"Existe conexión entre '{origen}' y '{destino}' (DFS)")
                else:
                    print(f"No hay conexión entre '{origen}' y '{destino}' (DFS)")
            
            elif opcion == "9":
                red.estadisticas()
            
            elif opcion == "0":
                print("Adioooos")
                break
            
            else:
                print("Opción no válida")
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu_principal()
