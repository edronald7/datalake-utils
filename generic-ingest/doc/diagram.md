# Framework de Ingesta de Datos en AWS – Data Lake

Este repositorio documenta un framework genérico y reutilizable para la **ingesta, transformación y publicación de datos** en un Data Lake sobre AWS. El objetivo es facilitar la incorporación de nuevos datasets de forma **escalable, gobernada y automatizada**, siguiendo buenas prácticas de arquitectura moderna.

---

## 🧱 Arquitectura General

La solución se organiza en **tres zonas principales**:

### 1. **Landing Zone**
- Punto de entrada de los datos crudos desde distintas fuentes (FTP, buckets externos, etc.).
- Los archivos `.csv.gz` son integrados con Apache NiFi y almacenados temporalmente en un bucket S3.
- Un **orquestador Lambda** se activa por eventos y consulta la configuración del dataset para decidir cómo procesarlo (job ligero o pesado).
- La configuración y cola de ingestas se almacenan en DynamoDB, lo que permite que el flujo sea completamente **dinámico y escalable**.

### 2. **Refined Zone**
- Los datos ya transformados son almacenados en un bucket separado.
- Se ejecutan procesos de transformación mediante:
  - **AWS Lambda** para cargas livianas.
  - **AWS Glue** para cargas pesadas (ETL complejas, grandes volúmenes).
- Los datasets se registran automáticamente en el **AWS Glue Data Catalog**, y quedan disponibles en **Athena** bajo la base `db_refined`.
- Se registran logs de ingesta y metadatos técnicos para trazabilidad.

### 3. **Trusted Zone**
- Se aplican validaciones de calidad mediante un job específico (`Job DataQuality`), donde se generan métricas de calidad y se notifican fallos (SNS).
- Luego se ejecuta el proceso de **anonimización**, aplicando enmascaramiento o eliminación de PII.
- Los datos finales se almacenan en un bucket confiable (`trusted`) y expuestos en Athena como `db_trusted_analytics`, para el acceso de usuarios analíticos.

---

## 🔄 Flujo de Datos

1. Los datos llegan desde FTPS o buckets externos → Apache NiFi los deposita en la **Landing Zone**.
2. Un trigger de evento activa un Lambda que consulta la configuración en DynamoDB y dirige el flujo.
3. Se ejecuta el job ETL (Lambda o Glue) → resultado se guarda en la **Refined Zone**.
4. Otro trigger activa el job de **Data Quality**.
5. Si pasa las validaciones, se ejecuta el job de **anonimización**.
6. El resultado final se publica en la **Trusted Zone**.

---

## 🧩 Componentes AWS utilizados

- **S3:** Almacenamiento por zonas (landing, refined, trusted).
- **Lambda:** Orquestación, procesamiento ligero, control de calidad, anonimización.
- **Glue:** Procesamiento ETL pesado y catálogo de datos.
- **Athena:** Consulta de datos por parte de usuarios y analistas.
- **DynamoDB:** Configuración de ingestas, colas, logs técnicos.
- **SNS:** Notificaciones sobre validaciones de calidad y errores.

---

## 🎯 Beneficios del Framework

- **Reutilizable:** Admite múltiples pipelines sin reescribir código.
- **Escalable:** Serverless y desacoplado, ideal para crecer con nuevos casos de uso.
- **Gobernado:** Control de calidad, anonimización y logs de trazabilidad incluidos.
- **Seguro:** Accesos controlados por zona, datos sensibles protegidos.
- **Auditable:** Métricas y catálogos automáticos con registro de cada paso.

---

## 🚀 Próximos pasos

- Establecer control de versiones y particiones por fecha de ingesta.
- Automatizar validaciones adicionales de esquema.
- Integrar monitoreo centralizado con CloudWatch.

---

## 👥 Público objetivo

Este framework está diseñado para:

- **Data Engineers** que necesiten incorporar nuevos orígenes de datos rápidamente.
- **Líderes técnicos** que buscan establecer una arquitectura de ingesta escalable y gobernada.
- **Analistas y Científicos de Datos**, que requieren acceso seguro a datos confiables y anonimizados.

---

## 📬 Contacto

Para dudas o contribuciones, por favor contacta al equipo de Data Engineering.

