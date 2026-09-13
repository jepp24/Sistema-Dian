# Sistema DIAN

Aplicación web para extraer las guías y cantidades de bultos de archivos PDF de la DIAN.

## Ejecutar localmente

Desde la carpeta `sistema Dian`:

```bash
python -m pip install -r requirements.txt
python app.py
```

La aplicación queda disponible en `http://localhost:5000`.

## Publicar con una URL permanente

El archivo `render.yaml` deja configurado un servicio web en Render. Para publicarlo:

1. Sube este repositorio a GitHub.
2. En Render, selecciona **New > Blueprint** y conecta el repositorio.
3. Confirma el servicio `sistema-dian` y espera el despliegue.
4. Render entregará una URL `onrender.com`. En **Settings > Custom Domains** puedes conectar tu dominio propio.

El plan `starter` mantiene el servicio activo. Un dominio propio debe registrarse con un proveedor de dominios y apuntarse a Render mediante DNS.
