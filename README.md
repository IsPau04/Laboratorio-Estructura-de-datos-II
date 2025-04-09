# Laboratorio-Estructura-de-datos-II
Solución a enunciado de laboratorio realizado en pyhton, utilizando arboles b, huffman, zlib, cryptography

INSTRUCCIONES: 
1. Descripción del problema
La empresa Talent Hub de Guatemala ha tenido buenas observaciones del proceso de cifrado de las
conversaciones de reclutamiento, debido que se ha fortalecido el acuerdo de confidencialidad entre la
persona y el reclutador, la cual lleva a tener un proceso seguro y de confianza en el proceso de
reclutamiento.
Por otro lado, Talent Hub compartió un dolor de negocio que se tiene actualmente, ya que durante el
proceso final de reclutamiento se comparte toda la información de la persona a la empresa. Sin embargo,
en algunas ocasiones se han enfrentado con personas que han falsificado su identidad, la cual menciona
que trabaja para una empresa cliente y requiere información de la persona.
Esto es un gran problema, debido que personas terceras obtiene información de las personas, robando
toda la información, además de incumplir el acuerdo de confidencialidad de Talent Hub con sus compañías
clientes, lo cual puede conllevar a cumplir grandes penalidades legales.
2. Recursos dependientes
La directora de Recursos humanos menciona que hoy en día cada reclutador solicita el carné de trabajo
para validar que la persona trabaje en una compañía cliente, posteriormente de la validación correcta, el
reclutador procede en darle toda la información de la persona, sin embargo, se ha observado que algunos
carnés de trabajos son fáciles de replicar.
3. Historia del usuario
Como directora de recurso humano, quiero tener una validación correcta de la identidad de los
reclutadores y de las compañías clientes, con la finalidad de proporcionarle toda la información del
proceso de reclutamiento a las personas correctas.
4. Aspectos a evaluar
El estudiante debe seleccionar el algoritmo de cifrado asimétrico correspondiente, tomando en
consideración los siguientes aspectos:
• Creación de la llave públicas a los clientes y reclutadores (25 Puntos).
• Creación de las llaves privadas a los clientes y reclutadores de talent hub (25 Puntos).
• Proceso de validación de identidad entre el cliente y reclutador, tomando en cuenta la llave
pública y privada (30 Puntos).
• Identificación de las vulnerabilidades de su proceso de validación de identidad (20 Puntos).
5. ¿Cómo se evaluará?
El estudiante recibirá como entrada una bitácora de datos (En un archivo .csv, separado por el
delimitador “;”), que le permitirá construir su estructura de datos:
• INSERT; JSON de persona
• PATCH: JSON con las llaves primaria y los atributos por modificar
• DELETE: JSON con las llaves primarias posteriormente
Posteriormente debe cargar una vista en donde debe seleccionar el reclutador y la compañía,
demostrando su proceso de validación de identidad.
Se debe tomar en cuenta que las creaciones de las llaves pública y privada se puede generar al momento
del inicio de carga de información (O en el momento que el estudiante le parece ideal).
De igual manera el proceso de validación de identidad lo puede realizar de cualquier forma, sin embargo,
debe tomar en cuenta la experiencia del usuario. (e.g. Pueden encriptar una palabra clave con la llave
pública, y al momento de desencriptar con la llave privada tanto el emisor y receptor debe coincidir la
misma palabra clave).
Observación: Se debe reutilizar el mismo código de los laboratorios anteriores.
