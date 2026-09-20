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
- **Dashboard**: Se ejecuta localmente mediante `streamlit run app.py`.
- **Sincronización**: Se ejecuta mediante scripts de Python (`sync_engine.py`) que pueden ser programados como tareas automáticas.
- **Keep-Alive**: Se ejecuta como un proceso en segundo plano (`keep_alive.py`) para mantener la conexión con Supabase.

---

## 2. Estado Actual del Proyecto (19/09/2026)

| Fase | Estado | Descripción |
| :--- | :--- | :--- |
| **Configuración** | ✅ Completado | Entorno, variables de entorno y conexión validadas. |
| **Estructura** | ✅ Completado | Proyecto `SYNC-NUBE-SUPABASE` inicializado en GitHub. |
| **Dashboard** | 🚧 En progreso | Interfaz básica creada, requiere integración total con funciones de push. |
| **Sincronización** | 🚧 En progreso | Lógica de combos implementada, falta validar contra datos reales. |
| **Automatización** | ✅ Completado | Script `keep_alive.py` listo. |

---

## 3. Próximos Pasos (Plan de Trabajo)
1. **Validación de Sincronización**: Comparar SKUs y datos entre Tiendanube y Supabase (incluye pruebas de flujo).
2. **Implementación de Push**: Habilitar la escritura desde Supabase hacia Tiendanube (incluye pruebas de flujo).
3. **Automatización y Monitoreo**: Configurar servicios permanentes (incluye pruebas de flujo).
4. **Capacitación y Gestión de Combos**: Pruebas finales de usuario (incluye pruebas de flujo).

*Nota: Cada paso incluye pruebas exhaustivas y requiere aprobación en Git.*
