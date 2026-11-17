# TP6 Interoperabilidad – Actividad 3 (Grupo 1: Encounter)
16.22 Informática Médica – ITBA
Delfina Cohen, Josefina Perez, Julian Haziel Granados García

## Patient
Creación del recurso paciente con algunos parámetros. Incluye el número de documento (DNI) como identifier, con el sistema de RENAPER.

## Encounter
Creación del recurso Encounter (encuentro clínico) asociado a un paciente mediante la referencia `Patient/{id}`.

## Base
Lectura y escritura de recursos en el servidor público de HAPI FHIR, y búsqueda de pacientes por DNI.

## Workflow
Desde acá se corre el código: crea el paciente (3.a), lo busca por DNI (3.b) y crea el Encounter (3.c).

