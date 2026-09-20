# Documento Maestro: Proyecto Sincronización Tiendanube-Supabase

## 1. Definición del Producto Final
El producto final es un **Sistema de Gestión de Inventario y Sincronización (Middleware)** que actúa como puente entre Tiendanube y Supabase. Su objetivo es centralizar la administración de productos, precios y combos, permitiendo una gestión masiva y automatizada.

### ¿Qué hace?
- **Sincronización Bidireccional**: Mantiene el stock y precios actualizados entre Tiendanube y Supabase.
- **Gestión de Combos**: Calcula automáticamente el stock disponible de combos basándose en el stock mínimo de sus componentes (materiales).
- **Dashboard de Gestión**: Interfaz (Streamlit) para visualizar productos, comparar datos, realizar ajustes masivos y gestionar combos.
- **Automatización**: Mantiene la base de datos de Supabase activa (evitando suspensión) y automatiza tareas de sincronización.

### ¿Qué se puede hacer en él?
- **Visualización**: Ver el estado actual de productos en ambas plataformas.
- **Actualización Masiva**: Impactar nuevos precios o stock mediante archivos Excel o ajustes directos en el dashboard.
- **Gestión de Combos**: Crear, editar y eliminar combos, con recálculo automático de stock.
- **Monitoreo**: Verificar logs de sincronización y estado de conexión.

### ¿Cómo se ejecuta?
- **Dashboard (Control Remoto)**: Streamlit actúa como interfaz para ejecutar los scripts de backend. No contiene lógica de negocio.
- **Motor (Backend)**: Scripts de Python (`01_pull_nube_to_db.py`, `2_push_nube.py`, etc.) que realizan las operaciones reales.
- **Lógica de Combos**: Implementada mediante Vistas SQL en Supabase para cálculo en tiempo real.
- **Automatización**: Webhooks para eventos en tiempo real y tareas programadas (cron) para auditoría diaria.

---

## 2. Estado Actual del Proyecto (20/09/2026)

| Fase | Estado | Descripción |
| :--- | :--- | :--- |
| **Configuración** | ✅ Completado | Entorno, variables de entorno y conexión validadas. |
| **Arquitectura** | 🚧 En progreso | Separación estricta entre Front (Streamlit) y Motor (Python/SQL). |
| **Dashboard** | 🚧 En progreso | Adaptación para actuar como "control remoto" de scripts. (Inventario y Combos en desarrollo) |
| **Sincronización** | ✅ Completado | Mejoras en la lógica de paginación en `api_tiendanube.py` para asegurar la cobertura total de registros, y ampliación del manejo de excepciones para incluir errores de conexión y timeout. Implementación de upsert masivo en `sync_nube_to_db.py` para optimizar la escritura a base de datos, incluyendo la lógica de negocio para precio y visibilidad (precio a $9.999.999 y `visible_en_web` a False si stock <= 0). Migración de lógica de combos a Vistas SQL **(en progreso)**.
| **Automatización** | 🚧 En progreso | Implementación de Webhooks y auditoría diaria. |

---

## 3. Próximos Pasos (Plan de Trabajo)
1. **Refactorización de Arquitectura**: Mover lógica de negocio del Dashboard a scripts de backend y Vistas SQL.
2. **Implementación de Vistas SQL**: Crear `vista_stock_combos` en Supabase.
3. **Integración de Scripts en Dashboard**: Configurar Streamlit para ejecutar scripts existentes (`01_pull`, `2_push`, `1_update`, etc.).
4. **Configuración de Webhooks**: Reemplazar sincronización constante por eventos disparados por Tiendanube.
5. **Auditoría y Monitoreo**: Configurar `sync_full.py` como tarea programada para auditoría diaria.

*Nota: Cada paso incluye pruebas exhaustivas y requiere aprobación en Git.*
