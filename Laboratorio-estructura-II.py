from BTrees._OOBTree import OOBTree
import csv
import json
import os
from collections import Counter
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import huffman
import zlib
import re
from cryptography.fernet import Fernet

# Crear una instancia de OOBTree
btree = OOBTree()

class Text:
    def __init__(self, title, text):
        self.title = self.extraer_dpi(title)
        self.text = text

    def extraer_dpi(self, nombre_archivo):
        # Busca una secuencia de 13 o más dígitos consecutivos que representaría el DPI
        match = re.search(r'\d{13,}', nombre_archivo)
        if match:
            return match.group(0)  # Retorna el DPI encontrado
        else:
            return nombre_archivo  # Si no encuentra un DPI, retorna el nombre original
        
    def __repr__(self):
        return f'Text(title={self.title}, text={self.text[:30]}...)'  # Solo mostrar los primeros 30 caracteres del texto para mejor visualización
    
def leer_archivos_de_carpeta(ruta_carpeta):
    lista_archivos = []
    

class Text:
    def __init__(self, title, text):
        self.title = title
        self.text = text

lista_conversaciones = []
lista_recomendaciones = []

def cargar_archivos_clasificados(ruta_carpeta):

    # Recorrer todos los archivos en la carpeta
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

        # Verificar que sea un archivo y que tenga extensión .txt
        if os.path.isfile(ruta_archivo) and nombre_archivo.endswith(".txt"):
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()

                # Obtener solo el DPI del nombre del archivo, eliminando el prefijo y la extensión
                dpi = nombre_archivo.split("-")[1].replace(".txt", "")
                
                # Crear una instancia de Text usando el DPI como título y el contenido como texto
                texto_archivo = Text(title=dpi, text=contenido)

                # Clasificar en las listas correspondientes según el prefijo
                if nombre_archivo.startswith("CONV-"):
                    lista_conversaciones.append(texto_archivo)
                elif nombre_archivo.startswith("REC-"):
                    lista_recomendaciones.append(texto_archivo)

    return lista_conversaciones, lista_recomendaciones


def leer_archivos_de_conversaciones(ruta_conversaciones):
    lista_archivos2 = []
    
    # Recorrer todos los archivos en la carpeta
    for nombre_archivo2 in os.listdir(ruta_conversaciones):
        ruta_archivo2 = os.path.join(ruta_conversaciones, nombre_archivo2)
        
        # Verificar que sea un archivo y que tenga extensión .txt
        if os.path.isfile(ruta_archivo2) and nombre_archivo2.endswith(".txt"):
            with open(ruta_archivo2, 'r', encoding='utf-8') as archivo2:
                contenido2 = archivo2.read()
                # Crear una instancia de Text usando el nombre del archivo (DPI) como título y el contenido como texto
                texto_archivo2 = Text(title=nombre_archivo2.replace(".txt", ""), text=contenido2)
                lista_archivos2.append(texto_archivo2)
    
    return lista_archivos2

class Metadata:
    def __init__(self, name, dpi, datebirth, address, recluiter, companies, binary_order=None, encoded_dpi=None):
        self.name = name
        self.dpi = dpi
        self.datebirth = datebirth
        self.address = address
        self.companies = companies
        self.binary_order = binary_order  # Para almacenar la representación binaria de las empresas
        self.encoded_dpi = encoded_dpi    # Para almacenar la representación binaria del DPI
        self.recluiter = recluiter
    def __repr__(self):
        return f'Metadata(name={self.name}, dpi={self.dpi}, datebirth={self.datebirth}, address={self.address}, binary_order={self.binary_order}, encoded_dpi={self.encoded_dpi})'

# Función para encriptar el contenido de un archivo
def encriptar_archivo(contenido):
    # Generar una clave de 256 bits (32 bytes) y un vector de inicialización
    key = os.urandom(32)
    iv = os.urandom(16)
    
    # Configurar cifrado AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Cifrar el contenido
    encrypted_data = encryptor.update(contenido.encode('utf-8')) + encryptor.finalize()

    return iv + encrypted_data  # Agregar IV al principio del archivo cifrado

def comprimir_archivo(contenido):
    contenido_bytes = contenido.encode('utf-8')  # Convertir a bytes
    contenido_comprimido = zlib.compress(contenido_bytes)
    return contenido_comprimido

# Función para descomprimir el contenido de un archivo
def descomprimir_archivo(contenido_comprimido):
    contenido_bytes = zlib.decompress(contenido_comprimido)
    return contenido_bytes.decode('utf-8')

# Función para validar la carpeta antes de descomprimir
def validar_carpeta_comprimidos(ruta_carpeta_comprimidos):
    # Verificar si la carpeta existe
    if not os.path.exists(ruta_carpeta_comprimidos):
        print("La carpeta no existe.")
        return False

    # Verificar si la carpeta está vacía o si no hay archivos con la extensión .zlib
    archivos_zlib = [f for f in os.listdir(ruta_carpeta_comprimidos) if f.endswith('.zlib')]
    if not archivos_zlib:
        print("La carpeta está vacía o no contiene archivos comprimidos .zlib.")
        return False
    
    return True

# Función principal que gestiona la validación de la carpeta
def gestionar_carpeta_comprimidos():
    while True:
        ruta_carpeta_comprimidos = input("Ingrese la ruta de la carpeta donde están los archivos comprimidos: ")
        
        if validar_carpeta_comprimidos(ruta_carpeta_comprimidos):
            # Si la validación es exitosa, continuar con la descompresión
            return ruta_carpeta_comprimidos
        else:
            cambiar_ruta = input("La carpeta no contiene archivos válidos. ¿Deseas cambiar la ruta? (sí/no): ").lower()
            if cambiar_ruta == "no":
                print("No existen archivos para descomprimir.")
                return None

# Función para descomprimir archivos (ya existente)
def descomprimir_archivos_en_carpeta(ruta_carpeta_comprimidos, ruta_carpeta_salida):
    if ruta_carpeta_comprimidos is None:
        return  # Si no se seleccionó ninguna carpeta, detener la operación

    # Asegurarse de que la carpeta de salida exista
    if not os.path.exists(ruta_carpeta_salida):
        os.makedirs(ruta_carpeta_salida)

    archivos_zlib = [f for f in os.listdir(ruta_carpeta_comprimidos) if f.endswith(".zlib")]

    for nombre_archivo in archivos_zlib:
        ruta_archivo_comprimido = os.path.join(ruta_carpeta_comprimidos, nombre_archivo)
        
        with open(ruta_archivo_comprimido, 'rb') as archivo_comprimido:
            contenido_comprimido = archivo_comprimido.read()

            # Descomprimir el contenido
            contenido_descomprimido = descomprimir_archivo(contenido_comprimido)

            # Crear la ruta completa para el archivo descomprimido
            nombre_archivo_descomprimido = nombre_archivo.replace("_comprimido.zlib", "_descomprimido.txt")
            ruta_archivo_descomprimido = os.path.join(ruta_carpeta_salida, nombre_archivo_descomprimido)

            with open(ruta_archivo_descomprimido, 'w', encoding='utf-8') as archivo_descomprimido:
                archivo_descomprimido.write(contenido_descomprimido)

            print(f"Archivo descomprimido guardado en {ruta_archivo_descomprimido}")

    print(f"Descompresión completada. Archivos descomprimidos guardados en {ruta_carpeta_salida}")

def buscar_y_comprimir_archivos_por_dpi(dpi_buscar, archivos):
    # Filtrar archivos que tengan el DPI específico
    archivos_encontrados = [archivo for archivo in archivos if archivo.title == dpi_buscar]

    if archivos_encontrados:
        print(f"Archivos encontrados para el DPI {dpi_buscar}: {[archivo.title for archivo in archivos_encontrados]}")

        # Definir el directorio donde se guardarán los archivos comprimidos
        carpeta_salida = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5/cartas de recomendacion/cartas comprimidas'
            
        # Asegurarse de que el directorio exista
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)

        rutas_comprimidas = []
        
        for i, archivo_encontrado in enumerate(archivos_encontrados, start=1):
            # Comprimir el archivo encontrado
            contenido_comprimido = comprimir_archivo(archivo_encontrado.text)

            # Crear la ruta completa para el archivo comprimido, añadiendo un número al final
            ruta_comprimida = os.path.join(carpeta_salida, f"{archivo_encontrado.title}_{i}_comprimido.zlib")

            # Guardar el archivo comprimido en la carpeta de salida
            with open(ruta_comprimida, 'wb') as f:
                f.write(contenido_comprimido)

            print(f"Archivo comprimido guardado en {ruta_comprimida}")
            rutas_comprimidas.append(ruta_comprimida)

        # Retornar las rutas de los archivos comprimidos
        return rutas_comprimidas
    else:
        print(f"No se encontraron archivos de texto para el DPI {dpi_buscar}")
        return None

# Generar y guardar la clave en un archivo
def generar_clave():
    key = Fernet.generate_key()
    with open("clave.key", "wb") as clave_file:
        clave_file.write(key)
    print("Clave generada y guardada en 'clave.key'.")

# Cargar la clave desde el archivo
def cargar_clave():
    with open("clave.key", "rb") as clave_file:
        return clave_file.read()

# Función para encriptar el contenido de un archivo
def encriptar_archivo(ruta_archivo):
    key = cargar_clave()
    fernet = Fernet(key)

    # Leer el contenido del archivo
    with open(ruta_archivo, "rb") as file:
        contenido = file.read()

    # Encriptar el contenido
    contenido_encriptado = fernet.encrypt(contenido)

    # Guardar el archivo encriptado
    ruta_archivo_encriptado = ruta_archivo + "_encriptado"
    with open(ruta_archivo_encriptado, "wb") as file_encriptado:
        file_encriptado.write(contenido_encriptado)
    print(f"Archivo encriptado guardado en {ruta_archivo_encriptado}")

# Función para buscar y encriptar los archivos de conversaciones por DPI
def buscar_y_encriptar_conversaciones_por_dpi(dpi, lista_conversaciones, ruta_encriptados):
    # Generar una clave de encriptación
    clave = Fernet.generate_key()
    fernet = Fernet(clave)
    
    # Asegurarse de que la carpeta de salida exista
    if not os.path.exists(ruta_encriptados):
        os.makedirs(ruta_encriptados)

    # Inicializar un contador para los archivos encriptados
    contador = 1

    # Recorrer la lista de conversaciones y encriptar las que coinciden con el DPI
    for conversacion in lista_conversaciones:
        if conversacion.title == dpi:
            contenido_bytes = conversacion.text.encode('utf-8')
            contenido_encriptado = fernet.encrypt(contenido_bytes)

            # Crear un nombre de archivo único usando el contador
            ruta_archivo_encriptado = os.path.join(ruta_encriptados, f"{conversacion.title}_{contador}.enc")
            contador += 1  # Incrementar el contador

            with open(ruta_archivo_encriptado, 'wb') as archivo_encriptado:
                archivo_encriptado.write(contenido_encriptado)

            print(f"Archivo encriptado guardado en {ruta_archivo_encriptado}")
    
    # También puedes imprimir o guardar la clave generada según necesites
    print(f"Clave de encriptación generada: {clave.decode('utf-8')}")

# Función para desencriptar el contenido de un archivo
def desencriptar_archivo(contenido_encriptado, clave):
    fernet = Fernet(clave)
    contenido_bytes = fernet.decrypt(contenido_encriptado)
    return contenido_bytes.decode('utf-8')

# Validar la existencia de la carpeta con archivos encriptados
def validar_carpeta_encriptados(ruta_carpeta_encriptados):
    if not os.path.exists(ruta_carpeta_encriptados):
        print("La carpeta no existe.")
        return False
    archivos_encriptados = [f for f in os.listdir(ruta_carpeta_encriptados) if os.path.isfile(os.path.join(ruta_carpeta_encriptados, f))]
    if not archivos_encriptados:
        print("La carpeta está vacía o no contiene archivos encriptados.")
        return False
    return True

# Función para gestionar la carpeta con archivos encriptados
def gestionar_carpeta_encriptados():
    while True:
        ruta_carpeta_encriptados = input("Ingrese la ruta de la carpeta donde están los archivos encriptados: ")
        if validar_carpeta_encriptados(ruta_carpeta_encriptados):
            return ruta_carpeta_encriptados
        else:
            cambiar_ruta = input("La carpeta no contiene archivos válidos. ¿Deseas cambiar la ruta? (sí/no): ").lower()
            if cambiar_ruta == "no":
                print("No existen archivos para desencriptar.")
                return None

def desencriptar_archivos_en_carpeta(ruta_carpeta_encriptados, carpeta_salida, clave):
    # Convertir la clave a un objeto Fernet para desencriptar
    fernet = Fernet(clave)
    
    # Asegurarse de que la carpeta de salida exista
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Recorrer los archivos en la carpeta de encriptados
    for nombre_archivo in os.listdir(ruta_carpeta_encriptados):
        ruta_archivo_encriptado = os.path.join(ruta_carpeta_encriptados, nombre_archivo)

        # Leer el contenido encriptado
        with open(ruta_archivo_encriptado, 'rb') as archivo_encriptado:
            contenido_encriptado = archivo_encriptado.read()

        # Desencriptar el contenido
        contenido_desencriptado = fernet.decrypt(contenido_encriptado)

        # Guardar el contenido desencriptado en la carpeta de salida
        nombre_archivo_desencriptado = nombre_archivo.replace('.enc', '_desencriptado.txt')
        ruta_archivo_desencriptado = os.path.join(carpeta_salida, nombre_archivo_desencriptado)
        
        with open(ruta_archivo_desencriptado, 'wb') as archivo_desencriptado:
            archivo_desencriptado.write(contenido_desencriptado)

        print(f"Archivo desencriptado guardado en {ruta_archivo_desencriptado}")

#LAB 5
class RegistroPersonaEmpresa:
    def __init__(self, nombre_persona, nombre_empresa, contenido_public, contenido_private):
        self.nombre_persona = nombre_persona
        self.nombre_empresa = nombre_empresa
        self.contenido_public = contenido_public
        self.contenido_private = contenido_private

    def __repr__(self):
        return f"Registro({self.nombre_persona}, {self.nombre_empresa}, Public: {self.contenido_public}, Private: {self.contenido_private})"

def leer_carpetas(ruta_principal):
    lista_registros = []

    # Recorrer cada subcarpeta en la carpeta principal
    for subcarpeta in os.listdir(ruta_principal):
        subcarpeta_ruta = os.path.join(ruta_principal, subcarpeta)
        if os.path.isdir(subcarpeta_ruta) and " - " in subcarpeta:
            nombre_persona, nombre_empresa = subcarpeta.split(" - ")

            # Leer archivos 'public.rsa' y 'private.rsa' en modo binario
            ruta_public = os.path.join(subcarpeta_ruta, "public.rsa")
            ruta_private = os.path.join(subcarpeta_ruta, "private.rsa")

            if os.path.isfile(ruta_public) and os.path.isfile(ruta_private):
                with open(ruta_public, 'rb') as f_public, open(ruta_private, 'rb') as f_private:
                    contenido_public = f_public.read()
                    contenido_private = f_private.read()

                registro = RegistroPersonaEmpresa(nombre_persona, nombre_empresa, contenido_public, contenido_private)
                lista_registros.append(registro)

    return lista_registros

# Paso 1: Contar la frecuencia de las compañías y los DPI
company_frequencies = Counter()
dpi_frequencies = Counter()

# Leer el archivo CSV y contar las frecuencias
with open('D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5/input5.csv') as csvfile:
    file = csv.reader(csvfile, delimiter=';')
    for line in file:
        if line[0] == "INSERT":
            data = json.loads(line[1])
            companies = data.get("companies")
            dpi = data.get("dpi")
            company_frequencies.update(companies)
            dpi_frequencies.update([dpi])  # Contar las veces que aparece cada DPI

# Paso 2: Generar los códigos de Huffman para las compañías y los DPI
huffman_company_codes = huffman.codebook(company_frequencies.items())
huffman_dpi_codes = huffman.codebook(dpi_frequencies.items())

# Leer el archivo CSV nuevamente y procesar los datos
with open('D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5/input5.csv') as csvfile:
    file = csv.reader(csvfile, delimiter=';')

    for line in file:
        if line[0] == "INSERT":
            data = json.loads(line[1])
            name = data.get("name")
            dpi = data.get("dpi")
            datebirth = data.get("datebirth")
            address = data.get("address")
            companies = data.get("companies")
            recluiter = data.get("recluiter")

            # Codificar las compañías y el DPI usando los códigos de Huffman
            encoded_companies = ''.join(huffman_company_codes[company] for company in companies if company in huffman_company_codes)
            #encoded_companies = ''.join(tmpLambda(companies, huffman_company_codes))
            encoded_dpi = huffman_dpi_codes[dpi] if dpi in huffman_dpi_codes else None
            
            # Crear una instancia de Metadata
            metadata_instance = Metadata(name, dpi, datebirth, address, companies,recluiter, binary_order=encoded_companies, encoded_dpi=encoded_dpi)
            

            btree[dpi] = metadata_instance  # Insertar en el Árbol B

            
        elif line[0] == "PATCH":
            data = json.loads(line[1])
            name = data.get("name")
            dpi = data.get("dpi")
            datebirth = data.get("datebirth")
            address = data.get("address")
            companies = data.get("companies")
            recluiter = data.get("recluiter")

            # Actualizar la entrada en el Árbol B
            if dpi in btree:
                encoded_companies = ''.join(huffman_company_codes[company] for company in companies if company in huffman_company_codes)
                encoded_dpi = huffman_dpi_codes[dpi] if dpi in huffman_dpi_codes else None
                metadata_instance = Metadata(name, dpi, datebirth, address, companies, recluiter, binary_order=encoded_companies, encoded_dpi=encoded_dpi)
                btree[dpi] = metadata_instance  # Actualizar en el Árbol B
            else:
                print(f'Error: No se encontró una entrada para name="{name}" y dpi="{dpi}". Acción PATCH no completada.')


        elif line[0] == "DELETE":
            data = json.loads(line[1])
            name = data.get("name")
            dpi = data.get("dpi")

            # Eliminar la entrada en el Árbol B
            if dpi in btree:
                del btree[dpi]
            else:
                print(f'Error: No se encontró una entrada para name="{name}" y dpi="{dpi}". Acción DELETE no completada.')

# Ejemplo de uso:
ruta_carpeta = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5/inputs rec y conv/inputs'
archivos = cargar_archivos_clasificados(ruta_carpeta)

#LAB 5
ruta_principal = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5/llaves/rsa'
registros = leer_carpetas(ruta_principal)

# Solicitar un DPI del usuario y buscarlo en el Árbol B
print("Hola, ¿Qué desea realizar?\n")


option = input("1. Codificar\n2. Decodificar\n")

if option == '1':
    search_dpi = input("Ingrese el DPI a buscar: ")
    results = [value for value in btree.values() if value.dpi.lower() == search_dpi.lower()]

    if results:
        print(f"Persona encontrada: {results[0].name}, DPI: {results[0].dpi}")

        # Solo llamar con la lista de conversaciones y encriptar sin solicitar clave ni ruta
        ruta_comprimida = buscar_y_comprimir_archivos_por_dpi(search_dpi, lista_conversaciones)

        if ruta_comprimida:
            print(f"Archivo comprimido correspondiente al DPI {search_dpi} está guardado en: {ruta_comprimida}")

        # Ruta predeterminada para guardar los archivos encriptados
        ruta_encriptados = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5/conversaciones/conversaciones encriptadas'

        # Encriptar las conversaciones automáticamente con una clave generada
        buscar_y_encriptar_conversaciones_por_dpi(search_dpi, lista_conversaciones, ruta_encriptados)

        print(f"Conversaciones encriptadas guardadas en {ruta_encriptados}")

    # Guardar resultados codificados en JSONL
    output_dir = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'resultadoscodificados.jsonl')
    with open(output_filename, 'w', encoding='utf-8') as jsonl_file:
        for result in results:
            result_dict = {
                "binary_order": result.binary_order,
                "encoded_dpi": result.encoded_dpi
            }
            jsonl_file.write(json.dumps(result_dict) + '\n')

    print(f"Resultados guardados en el archivo '{output_filename}'")
    
elif option == '2':
    binary_input = input("Ingrese el código binario de las empresas a decodificar: ")

    # Decodificar las empresas buscando en los códigos Huffman
    decoded_companies = [company for company, code in huffman_company_codes.items() if binary_input.startswith(code)]
    
    if decoded_companies:
        # Buscar todas las personas que tengan las mismas empresas
        matching_people = [person for person in btree.values() if ''.join(huffman_company_codes[company] for company in person.companies) == binary_input]
        
        # Si hay más de una persona con las mismas empresas, validar con el DPI
        if len(matching_people) > 1:
            print("Se encontraron varias personas con las mismas empresas.")
            encoded_dpi_input = input("Ingrese el código binario del DPI: ")
            
            # Buscar la persona que coincida con el DPI codificado
            matching_person = next((person for person in matching_people if person.encoded_dpi == encoded_dpi_input), None)
            
            if matching_person:
                print(f"Persona encontrada: {matching_person.name}, DPI: {matching_person.dpi}, Nacimiento: {matching_person.datebirth}, Dirección: {matching_person.address}")

                # Guardar el resultado en un archivo JSONL
                output_dir = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_filename = os.path.join(output_dir, 'resultados_decodificados.jsonl')

                with open(output_filename, 'w', encoding='utf-8') as jsonl_file:
                    result_dict = {
                        "name": matching_person.name,
                        "dpi": matching_person.dpi,
                        "datebirth": matching_person.datebirth,
                        "address": matching_person.address,
                        "companies": matching_person.companies
                    }
                    jsonl_file.write(json.dumps(result_dict) + '\n')

                print(f'Resultados guardados en el archivo "{output_filename}".')

            else:
                print("No se encontró ninguna persona con ese DPI y empresas.")
        elif len(matching_people) == 1:
            matching_person = matching_people[0]


            # Guardar el resultado en un archivo JSONL
            output_dir = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_filename = os.path.join(output_dir, 'resultados_decodificados.jsonl')

            with open(output_filename, 'w', encoding='utf-8') as jsonl_file:
                result_dict = {
                    "name": matching_person.name,
                    "dpi": matching_person.dpi,
                    "datebirth": matching_person.datebirth,
                    "address": matching_person.address,
                    "companies": matching_person.companies
                }
                jsonl_file.write(json.dumps(result_dict) + '\n')

            print(f'Resultados guardados en el archivo "{output_filename}".')

        else:
            print("No se encontró ninguna persona con esas empresas.")
    else:
        print("No se pudo decodificar.")

    # Solicitar la ruta de la carpeta donde están los archivos comprimidos
    ruta_carpeta_comprimidos = gestionar_carpeta_comprimidos()

    # Definir la carpeta de salida para los archivos descomprimidos
    ruta_carpeta_salida = 'D:/UNIVERSIDAD/CUARTO SEMESTRE/Estructura de datos II/Lab 5/cartas de recomendación/cartas descomprimidas'

    # Llamar a la función para descomprimir los archivos
    descomprimir_archivos_en_carpeta(ruta_carpeta_comprimidos, ruta_carpeta_salida)

# Solicitar clave y carpeta con archivos encriptados
    clave = input("Ingrese la clave de desencriptación: ").encode()
    ruta_carpeta_encriptados = gestionar_carpeta_encriptados()
            
        # Validar clave y desencriptar archivos en carpeta
    if ruta_carpeta_encriptados:
        carpeta_salida = input("Ingrese la ruta de la carpeta para guardar los archivos desencriptados: ")
        desencriptar_archivos_en_carpeta(ruta_carpeta_encriptados, carpeta_salida, clave)
