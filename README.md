# 🚀 EC2 Auto Deploy

Script en Python para automatizar el despliegue de instancias EC2 en AWS con Apache preinstalado.

## 📋 Requisitos

- Python 3.10+
- Cuenta de AWS con permisos sobre EC2
- AWS CLI configurado

```bash
pip install boto3
```

## ⚙️ Configuración

Antes de correr el script, asegurate de actualizar las siguientes variables en `deploy.py`:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `REGION` | Región de AWS | `us-east-1` |
| `VpcId` | ID de tu VPC | `vpc-xxxxxxxxx` |
| `group-name` | Nombre del security group existente | `hola que tal` |
| `ImageId` | AMI a usar | `ami-xxxxxxxxx` |

## 🚀 Uso

```bash
python deploy.py --name <nombre-instancia> [--type <tipo-instancia>]
```

### Parámetros

| Parámetro | Requerido | Default | Descripción |
|---|---|---|---|
| `--name` | ✅ Sí | — | Nombre de la instancia EC2 |
| `--type` | ❌ No | `t3.micro` | Tipo de instancia EC2 |

### Ejemplos

```bash
# Instancia con configuración por defecto (t3.micro)
python deploy.py --name mi-servidor

# Instancia con tipo personalizado
python deploy.py --name mi-servidor --type t3.small
```

## 🔄 ¿Qué hace el script?

```
1. Obtiene el Security Group de la VPC configurada
2. Crea una instancia EC2 con Apache (httpd) preinstalado
3. Espera hasta que la instancia esté en estado "running"
4. Muestra la IP pública de la instancia
```

## 📄 User Data

Al iniciar, la instancia ejecuta automáticamente:

- Actualización del sistema (`yum update`)
- Instalación y arranque de Apache (`httpd`)
- Creación de una página HTML con el nombre y fecha de creación de la instancia

Una vez corriendo, podés acceder desde el navegador:

```
http://<IP_PUBLICA>
```

## 🗂️ Estructura del proyecto

```
python-proyects/
│
├── deploy.py       # Script principal
├── README.md       # Este archivo
└── venv/           # Entorno virtual
```

## 🔐 Autenticación AWS

El script usa las credenciales configuradas en tu entorno. Podés configurarlas de las siguientes formas:

```bash
# Opción 1 - AWS CLI (recomendado)
aws configure

# Opción 2 - Variables de entorno
export AWS_ACCESS_KEY_ID=tu-key
export AWS_SECRET_ACCESS_KEY=tu-secret
export AWS_DEFAULT_REGION=us-east-1
```
