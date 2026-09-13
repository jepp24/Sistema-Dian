# Sistema DIAN

Aplicación web para extraer las guías y cantidades de bultos de archivos PDF de la DIAN.

## 🌐 Despliegue en GitHub Pages

✅ Este repositorio está configurado para desplegar automáticamente en GitHub Pages.

**URL de despliegue:** https://jepp24.github.io/Sistema-Dian/

El despliegue se ejecuta automáticamente cada vez que haces push a la rama `main`. Puedes ver el progreso en la pestaña **Actions** de tu repositorio.

## Ejecutar localmente

Desde la carpeta `sistema Dian`:

```bash
python -m pip install -r requirements.txt
python app.py
```

La aplicación queda disponible en `http://localhost:5000`.

## Publicar con una URL permanente (alternativo)

El archivo `render.yaml` deja configurado un servicio web en Render. Para publicarlo:

1. Sube este repositorio a GitHub.
2. En Render, selecciona **New > Blueprint** y conecta el repositorio.
3. Confirma el servicio `sistema-dian` y espera el despliegue.
4. Render entregará una URL `onrender.com`. En **Settings > Custom Domains** puedes conectar tu dominio propio.

El plan `starter` mantiene el servicio activo. Un dominio propio debe registrarse con un proveedor de dominios y apuntarse a Render mediante DNS.
